from pathlib import Path

from lxml import etree

from opnsense_config_generator.builders.aliases import build_aliases
from opnsense_config_generator.builders.bridges import build_bridges
from opnsense_config_generator.builders.certs import build_certs_config
from opnsense_config_generator.builders.acme_client import build_acme_client
from opnsense_config_generator.builders.bind import build_bind
from opnsense_config_generator.builders.chrony import build_chrony
from opnsense_config_generator.builders.cron import build_cron
from opnsense_config_generator.builders.git_backup import build_git_backup
from opnsense_config_generator.builders.monit import build_monit
from opnsense_config_generator.builders.radvd import build_radvd
from opnsense_config_generator.builders.trafficshaper import build_trafficshaper
from opnsense_config_generator.builders.dnsmasq import build_dnsmasq
from opnsense_config_generator.builders.filter import build_filter
from opnsense_config_generator.builders.gateways import build_gateways
from opnsense_config_generator.builders.interfaces import build_interfaces
from opnsense_config_generator.builders.ipsec import build_ipsec
from opnsense_config_generator.builders.laggs import build_laggs
from opnsense_config_generator.builders.nat import build_nat
from opnsense_config_generator.builders.ntpd import build_ntpd
from opnsense_config_generator.builders.openvpn import build_openvpn
from opnsense_config_generator.builders.kea import build_kea
from opnsense_config_generator.builders.qemu_guest_agent import build_qemu_guest_agent
from opnsense_config_generator.builders.routes import build_staticroutes
from opnsense_config_generator.builders.syslog import build_syslog
from opnsense_config_generator.builders.system import build_system
from opnsense_config_generator.builders.unbound import build_unbound
from opnsense_config_generator.builders.vlans import build_vlans
from opnsense_config_generator.builders.wireguard import build_wireguard
from opnsense_config_generator.models.root import OpnSenseConfig
from opnsense_config_generator.render import render_template
from opnsense_config_generator.revision import build_revision_block
from opnsense_config_generator.version import OPNSENSE_VERSION
from opnsense_config_generator.xml_utils import make_root, serialize, sub


def build_xml(cfg: OpnSenseConfig) -> bytes:
    root = make_root()

    sub(root, "version", OPNSENSE_VERSION)
    sub(root, "lastchange")

    system_el = build_system(cfg.system)
    if (git_el := build_git_backup(cfg.git_backup)) is not None:
        backup_el = etree.SubElement(system_el, "backup")
        backup_el.append(git_el)
    root.append(system_el)
    root.append(build_interfaces(cfg.interfaces))

    # Legacy: CA and cert entries go directly under <opnsense>
    cas, certs = build_certs_config(cfg.certs)
    for el in cas:
        root.append(el)
    for el in certs:
        root.append(el)

    for optional in [
        build_vlans(cfg.vlans),
        build_bridges(cfg.bridges),
        build_laggs(cfg.laggs),
        build_gateways(cfg.gateways),
        build_staticroutes(cfg.staticroutes),
        build_aliases(cfg.aliases),
    ]:
        if optional is not None:
            root.append(optional)

    root.append(build_filter(cfg.filter))
    root.append(build_nat(cfg.nat))

    dnsmasq = build_dnsmasq(cfg.dnsmasq)
    if dnsmasq is not None:
        root.append(dnsmasq)

    root.append(build_unbound(cfg.unbound))

    rrd = etree.SubElement(root, "rrd")
    etree.SubElement(rrd, "enable")

    ntpd = build_ntpd(cfg.ntpd)
    if ntpd is not None:
        root.append(ntpd)

    # MVC plugins go under <OPNsense>
    mvc_children = []
    for builder, mvc_cfg in [
        (build_wireguard, cfg.wireguard),
        (build_openvpn, cfg.openvpn),
        (build_ipsec, cfg.ipsec),
        (build_cron, cfg.cron),
        (build_monit, cfg.monit),
        (build_trafficshaper, cfg.trafficshaper),
        (build_radvd, cfg.radvd),
        (build_kea, cfg.kea),
        (build_qemu_guest_agent, cfg.qemu_guest_agent),
        (build_acme_client, cfg.acme_client),
        (build_bind, cfg.bind),
        (build_chrony, cfg.chrony),
    ]:
        el = builder(mvc_cfg)  # type: ignore[operator]
        if el is not None:
            mvc_children.append(el)

    # Syslog is always emitted (has general settings)
    mvc_children.append(build_syslog(cfg.syslog))

    if mvc_children:
        opnsense_el = etree.SubElement(root, "OPNsense")
        for child in mvc_children:
            opnsense_el.append(child)

    root.append(build_revision_block())

    return serialize(root)


def run_pipeline(
    template_path: Path,
    intermediate_path: Path,
    output_path: Path,
) -> None:
    raw = render_template(template_path, intermediate_path)
    cfg = OpnSenseConfig.model_validate(raw)
    xml_bytes = build_xml(cfg)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(xml_bytes)
