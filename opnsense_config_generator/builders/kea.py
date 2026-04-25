from lxml import etree

from opnsense_config_generator.builders.base import bool_val
from opnsense_config_generator.models.kea import (
    KeaConfig,
    KeaCtrlAgentConfig,
    KeaDdnsConfig,
    KeaDhcpv4Config,
    KeaDhcpv6Config,
)
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub


def _subnet4_uuid(cidr: str) -> str:
    return make_uuid("kea:subnet4", cidr)


def _subnet6_uuid(cidr: str) -> str:
    return make_uuid("kea:subnet6", cidr)


def _reservation4_uuid(subnet: str, hw_address: str) -> str:
    return make_uuid("kea:reservation4", f"{subnet}:{hw_address}")


def _reservation6_uuid(subnet: str, identifier: str) -> str:
    return make_uuid("kea:reservation6", f"{subnet}:{identifier}")


def _build_dhcp4(cfg: KeaDhcpv4Config) -> etree._Element:
    el = etree.Element("dhcp4")

    gen = etree.SubElement(el, "general")
    sub(gen, "enabled", bool_val(cfg.enabled))
    sub(gen, "interfaces", ",".join(cfg.interfaces))
    sub(gen, "valid_lifetime", str(cfg.valid_lifetime))
    sub(gen, "fwrules", bool_val(cfg.fwrules))

    subnets_el = etree.SubElement(el, "subnets")
    for sn in cfg.subnets:
        uid = _subnet4_uuid(sn.subnet)
        s = etree.SubElement(subnets_el, "subnet4", uuid=uid)
        sub(s, "subnet", sn.subnet)
        sub(s, "option_data_autocollect", bool_val(sn.option_data_autocollect))
        if sn.pools:
            sub(s, "pools", ",".join(sn.pools))
        od = sn.option_data
        has_options = any([
            od.routers, od.domain_name_servers, od.domain_name,
            od.domain_search, od.ntp_servers, od.tftp_server_name, od.boot_file_name,
        ])
        if has_options:
            opt_el = etree.SubElement(s, "option_data")
            if od.routers:
                sub(opt_el, "routers", od.routers)
            if od.domain_name_servers:
                sub(opt_el, "domain_name_servers", ",".join(od.domain_name_servers))
            if od.domain_name:
                sub(opt_el, "domain_name", od.domain_name)
            if od.domain_search:
                sub(opt_el, "domain_search", ",".join(od.domain_search))
            if od.ntp_servers:
                sub(opt_el, "ntp_servers", ",".join(od.ntp_servers))
            if od.tftp_server_name:
                sub(opt_el, "tftp_server_name", od.tftp_server_name)
            if od.boot_file_name:
                sub(opt_el, "boot_file_name", od.boot_file_name)
        if sn.description:
            sub(s, "description", sn.description)

    reservations_el = etree.SubElement(el, "reservations")
    for res in cfg.reservations:
        uid = _reservation4_uuid(res.subnet, res.hw_address)
        r = etree.SubElement(reservations_el, "reservation", uuid=uid)
        sub(r, "subnet", _subnet4_uuid(res.subnet))
        sub(r, "hw_address", res.hw_address)
        if res.ip_address:
            sub(r, "ip_address", res.ip_address)
        if res.hostname:
            sub(r, "hostname", res.hostname)
        if res.description:
            sub(r, "description", res.description)

    return el


def _build_dhcp6(cfg: KeaDhcpv6Config) -> etree._Element:
    el = etree.Element("dhcp6")

    gen = etree.SubElement(el, "general")
    sub(gen, "enabled", bool_val(cfg.enabled))
    sub(gen, "interfaces", ",".join(cfg.interfaces))
    sub(gen, "valid_lifetime", str(cfg.valid_lifetime))
    sub(gen, "fwrules", bool_val(cfg.fwrules))

    subnets_el = etree.SubElement(el, "subnets")
    for sn in cfg.subnets:
        uid = _subnet6_uuid(sn.subnet)
        s = etree.SubElement(subnets_el, "subnet6", uuid=uid)
        sub(s, "subnet", sn.subnet)
        if sn.interface:
            sub(s, "interface", sn.interface)
        if sn.pools:
            sub(s, "pools", ",".join(sn.pools))
        od = sn.option_data
        has_options = any([od.dns_servers, od.domain_search])
        if has_options:
            opt_el = etree.SubElement(s, "option_data")
            if od.dns_servers:
                sub(opt_el, "dns_servers", ",".join(od.dns_servers))
            if od.domain_search:
                sub(opt_el, "domain_search", ",".join(od.domain_search))
        if sn.description:
            sub(s, "description", sn.description)

    reservations_el = etree.SubElement(el, "reservations")
    for res in cfg.reservations:
        identifier = res.duid or res.hw_address
        uid = _reservation6_uuid(res.subnet, identifier)
        r = etree.SubElement(reservations_el, "reservation", uuid=uid)
        sub(r, "subnet", _subnet6_uuid(res.subnet))
        if res.duid:
            sub(r, "duid", res.duid)
        if res.hw_address:
            sub(r, "hw_address", res.hw_address)
        if res.ip_address:
            sub(r, "ip_address", res.ip_address)
        if res.hostname:
            sub(r, "hostname", res.hostname)
        if res.description:
            sub(r, "description", res.description)

    return el


def _build_ctrl_agent(cfg: KeaCtrlAgentConfig) -> etree._Element:
    el = etree.Element("ctrl_agent")
    gen = etree.SubElement(el, "general")
    sub(gen, "enabled", bool_val(cfg.enabled))
    sub(gen, "http_host", cfg.http_host)
    sub(gen, "http_port", cfg.http_port)
    return el


def _build_ddns(cfg: KeaDdnsConfig) -> etree._Element:
    el = etree.Element("ddns")
    gen = etree.SubElement(el, "general")
    sub(gen, "enabled", bool_val(cfg.enabled))
    sub(gen, "server_ip", cfg.server_ip)
    sub(gen, "server_port", cfg.server_port)
    return el


def build_kea(cfg: KeaConfig) -> etree._Element | None:
    if not any([cfg.dhcp4.enabled, cfg.dhcp6.enabled, cfg.ctrl_agent.enabled, cfg.ddns.enabled]):
        return None

    el = etree.Element("Kea")
    el.append(_build_dhcp4(cfg.dhcp4))
    el.append(_build_dhcp6(cfg.dhcp6))
    el.append(_build_ctrl_agent(cfg.ctrl_agent))
    el.append(_build_ddns(cfg.ddns))
    return el
