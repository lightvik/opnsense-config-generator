from lxml import etree

from opnsense_config_generator.models.dnsmasq import DnsmasqConfig
from opnsense_config_generator.xml_utils import sub


def build_dnsmasq(cfg: DnsmasqConfig) -> etree._Element | None:
    if not cfg.enable and not cfg.dhcp_ranges:
        return None

    dnsmasq = etree.Element("dnsmasq")

    if cfg.enable:
        sub(dnsmasq, "enable", "1")
    sub(dnsmasq, "port", cfg.port)
    if cfg.interface:
        sub(dnsmasq, "interface", cfg.interface)

    dhcp_el = etree.SubElement(dnsmasq, "dhcp")
    if cfg.dhcp.enable_ra:
        sub(dhcp_el, "enable_ra", "1")

    for r in cfg.dhcp_ranges:
        range_el = etree.SubElement(dnsmasq, "dhcp_ranges")
        sub(range_el, "interface", r.interface)
        sub(range_el, "start_addr", r.start_addr)
        sub(range_el, "end_addr", r.end_addr)
        if r.constructor:
            sub(range_el, "constructor", r.constructor)
        if r.ra_mode:
            sub(range_el, "ra_mode", r.ra_mode)

    if cfg.regdhcp:
        sub(dnsmasq, "regdhcp", "1")
    if cfg.regdhcpstatic:
        sub(dnsmasq, "regdhcpstatic", "1")
    if cfg.strict_order:
        sub(dnsmasq, "strict_order", "1")

    return dnsmasq
