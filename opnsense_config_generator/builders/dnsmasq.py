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
    if cfg.dhcpfirst:
        sub(dnsmasq, "dhcpfirst")
    if cfg.domain_needed:
        sub(dnsmasq, "domain_needed")
    if cfg.no_private_reverse:
        sub(dnsmasq, "no_private_reverse")
    if cfg.no_resolv:
        sub(dnsmasq, "no_resolv")
    if cfg.log_queries:
        sub(dnsmasq, "log_queries")
    if cfg.no_hosts:
        sub(dnsmasq, "no_hosts")
    if cfg.strictbind:
        sub(dnsmasq, "strictbind")
    if cfg.dnssec:
        sub(dnsmasq, "dnssec")
    if cfg.add_mac:
        sub(dnsmasq, "add_mac")
    if cfg.regdhcpdomain:
        sub(dnsmasq, "regdhcpdomain", cfg.regdhcpdomain)
    if cfg.dns_forward_max is not None:
        sub(dnsmasq, "dns_forward_max", str(cfg.dns_forward_max))
    if cfg.cache_size is not None:
        sub(dnsmasq, "cache_size", str(cfg.cache_size))
    if cfg.local_ttl is not None:
        sub(dnsmasq, "local_ttl", str(cfg.local_ttl))

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

    for host in cfg.hosts:
        h = etree.SubElement(dnsmasq, "hosts")
        sub(h, "host", host.host)
        sub(h, "domain", host.domain)
        sub(h, "ip", host.ip)
        if host.descr:
            sub(h, "descr", host.descr)
        if host.mac:
            sub(h, "mac", host.mac)

    for override in cfg.domainoverrides:
        d = etree.SubElement(dnsmasq, "domainoverrides")
        sub(d, "domain", override.domain)
        sub(d, "ip", override.ip)
        if override.descr:
            sub(d, "descr", override.descr)

    for opt in cfg.dhcp_options:
        o = etree.SubElement(dnsmasq, "dhcp_options")
        if opt.tag:
            sub(o, "tag", opt.tag)
        sub(o, "number", opt.number)
        if opt.value:
            sub(o, "value", opt.value)

    if cfg.regdhcp:
        sub(dnsmasq, "regdhcp", "1")
    if cfg.regdhcpstatic:
        sub(dnsmasq, "regdhcpstatic", "1")
    if cfg.strict_order:
        sub(dnsmasq, "strict_order", "1")

    return dnsmasq
