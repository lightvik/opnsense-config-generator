"""Snapshot tests: per-section YAML → per-section XML fragment."""

from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml
from lxml import etree
from pydantic import BaseModel

from opnsense_config_generator.builders.acme_client import build_acme_client
from opnsense_config_generator.builders.bind import build_bind
from opnsense_config_generator.builders.chrony import build_chrony
from opnsense_config_generator.builders.cron import build_cron
from opnsense_config_generator.builders.dnsmasq import build_dnsmasq
from opnsense_config_generator.builders.filter import build_filter
from opnsense_config_generator.builders.git_backup import build_git_backup
from opnsense_config_generator.builders.interfaces import build_interfaces
from opnsense_config_generator.builders.ipsec import build_ipsec
from opnsense_config_generator.builders.kea import build_kea
from opnsense_config_generator.builders.monit import build_monit
from opnsense_config_generator.builders.ntpd import build_ntpd
from opnsense_config_generator.builders.openvpn import build_openvpn
from opnsense_config_generator.builders.qemu_guest_agent import build_qemu_guest_agent
from opnsense_config_generator.builders.radvd import build_radvd
from opnsense_config_generator.builders.syslog import build_syslog
from opnsense_config_generator.builders.system import build_system
from opnsense_config_generator.builders.trafficshaper import build_trafficshaper
from opnsense_config_generator.builders.wireguard import build_wireguard
from opnsense_config_generator.models.acme_client import AcmeClientConfig
from opnsense_config_generator.models.bind import BindConfig
from opnsense_config_generator.models.chrony import ChronyConfig
from opnsense_config_generator.models.cron import CronConfig
from opnsense_config_generator.models.dnsmasq import DnsmasqConfig
from opnsense_config_generator.models.filter import FilterConfig
from opnsense_config_generator.models.git_backup import GitBackupConfig
from opnsense_config_generator.models.interfaces import InterfacesConfig
from opnsense_config_generator.models.ipsec import IpsecConfig
from opnsense_config_generator.models.kea import KeaConfig
from opnsense_config_generator.models.monit import MonitConfig
from opnsense_config_generator.models.ntpd import NtpdConfig
from opnsense_config_generator.models.openvpn import OpenVpnConfig
from opnsense_config_generator.models.qemu_guest_agent import QemuGuestAgentConfig
from opnsense_config_generator.models.radvd import RadvdConfig
from opnsense_config_generator.models.syslog import SyslogConfig
from opnsense_config_generator.models.system import SystemConfig
from opnsense_config_generator.models.trafficshaper import TrafficShaperConfig
from opnsense_config_generator.models.wireguard import WireguardConfig

SNAPSHOTS_DIR = Path(__file__).parent / "snapshots"


def _xml_str(el: etree._Element) -> str:
    etree.indent(el, space="  ")
    return etree.tostring(el, pretty_print=True, encoding="unicode")


def _snapshot_test(
    section: str,
    build_fn: Callable[..., Any],
    model_cls: type[BaseModel],
    update: bool,
    fixture: str = "basic",
) -> None:
    snap_dir = SNAPSHOTS_DIR / section
    input_yaml = snap_dir / f"{fixture}.yaml"
    expected_xml = snap_dir / f"{fixture}.expected.xml"

    if not input_yaml.exists():
        return

    data = yaml.safe_load(input_yaml.read_text())
    model = model_cls.model_validate(data)
    result = build_fn(model)

    actual = "" if result is None else _xml_str(result)

    if update or not expected_xml.exists():
        expected_xml.write_text(actual)
        return

    assert actual == expected_xml.read_text(), (
        f"Snapshot mismatch for {section}/basic. Run with --update-snapshots."
    )


def test_snapshot_cron(update_snapshots: bool) -> None:
    _snapshot_test("cron", build_cron, CronConfig, update_snapshots)


def test_snapshot_monit(update_snapshots: bool) -> None:
    _snapshot_test("monit", build_monit, MonitConfig, update_snapshots)


def test_snapshot_radvd(update_snapshots: bool) -> None:
    _snapshot_test("radvd", build_radvd, RadvdConfig, update_snapshots)


def test_snapshot_trafficshaper(update_snapshots: bool) -> None:
    _snapshot_test("trafficshaper", build_trafficshaper, TrafficShaperConfig, update_snapshots)


def test_snapshot_dnsmasq(update_snapshots: bool) -> None:
    _snapshot_test("dnsmasq", build_dnsmasq, DnsmasqConfig, update_snapshots)


def test_snapshot_system(update_snapshots: bool) -> None:
    _snapshot_test("system", build_system, SystemConfig, update_snapshots)


def test_snapshot_interfaces(update_snapshots: bool) -> None:
    _snapshot_test("interfaces", build_interfaces, InterfacesConfig, update_snapshots)


def test_snapshot_filter(update_snapshots: bool) -> None:
    _snapshot_test("filter", build_filter, FilterConfig, update_snapshots)


def test_snapshot_ntpd(update_snapshots: bool) -> None:
    _snapshot_test("ntpd", build_ntpd, NtpdConfig, update_snapshots)


def test_snapshot_wireguard(update_snapshots: bool) -> None:
    _snapshot_test("wireguard", build_wireguard, WireguardConfig, update_snapshots)


def test_snapshot_openvpn(update_snapshots: bool) -> None:
    _snapshot_test("openvpn", build_openvpn, OpenVpnConfig, update_snapshots)


def test_snapshot_ipsec(update_snapshots: bool) -> None:
    _snapshot_test("ipsec", build_ipsec, IpsecConfig, update_snapshots)


def test_snapshot_syslog(update_snapshots: bool) -> None:
    _snapshot_test("syslog", build_syslog, SyslogConfig, update_snapshots)


def test_snapshot_kea_basic(update_snapshots: bool) -> None:
    _snapshot_test("kea", build_kea, KeaConfig, update_snapshots)


def test_snapshot_kea_with_reservations(update_snapshots: bool) -> None:
    _snapshot_test("kea", build_kea, KeaConfig, update_snapshots, fixture="with_reservations")


def test_snapshot_qemu_guest_agent_basic(update_snapshots: bool) -> None:
    _snapshot_test(
        "qemu_guest_agent", build_qemu_guest_agent, QemuGuestAgentConfig, update_snapshots
    )


def test_snapshot_qemu_guest_agent_disabled_rpcs(update_snapshots: bool) -> None:
    _snapshot_test(
        "qemu_guest_agent",
        build_qemu_guest_agent,
        QemuGuestAgentConfig,
        update_snapshots,
        fixture="with_disabled_rpcs",
    )


def test_snapshot_acme_client(update_snapshots: bool) -> None:
    _snapshot_test("acme_client", build_acme_client, AcmeClientConfig, update_snapshots)


def test_snapshot_bind(update_snapshots: bool) -> None:
    _snapshot_test("bind", build_bind, BindConfig, update_snapshots)


def test_snapshot_chrony(update_snapshots: bool) -> None:
    _snapshot_test("chrony", build_chrony, ChronyConfig, update_snapshots)


def test_snapshot_git_backup(update_snapshots: bool) -> None:
    _snapshot_test("git_backup", build_git_backup, GitBackupConfig, update_snapshots)
