from lxml import etree

from opnsense_config_generator.models.unbound import UnboundConfig
from opnsense_config_generator.xml_utils import sub


def build_unbound(cfg: UnboundConfig) -> etree._Element:
    unbound = etree.Element("unbound")
    if cfg.enable:
        sub(unbound, "enable", "1")
    if cfg.dnssec:
        sub(unbound, "dnssec")
    if cfg.forwarding:
        sub(unbound, "forwarding")
    if cfg.forward_tls_upstream:
        sub(unbound, "forward_tls_upstream")
    if cfg.active_interface:
        sub(unbound, "active_interface", cfg.active_interface)
    if cfg.outgoing_interface:
        sub(unbound, "outgoing_interface", cfg.outgoing_interface)
    if cfg.hide_identity:
        sub(unbound, "hideidentity")
    if cfg.hide_version:
        sub(unbound, "hideversion")
    if cfg.prefetch:
        sub(unbound, "prefetch")
    if cfg.prefetch_key:
        sub(unbound, "prefetchkey")
    if cfg.dns64:
        sub(unbound, "dns64")
    if cfg.log_queries:
        sub(unbound, "log_verbosity", "2")
    if cfg.cache_max_ttl != 86400:
        sub(unbound, "cache_max_ttl", str(cfg.cache_max_ttl))
    if cfg.cache_min_ttl:
        sub(unbound, "cache_min_ttl", str(cfg.cache_min_ttl))
    for server in cfg.forward_servers:
        sub(unbound, "forwarder", server)
    for host in cfg.hosts:
        h = etree.SubElement(unbound, "hosts")
        sub(h, "host", host.host)
        sub(h, "domain", host.domain)
        sub(h, "ip", host.ip)
        if host.descr:
            sub(h, "descr", host.descr)
        for alias in host.aliases:
            sub(h, "aliases", alias)
    for override in cfg.domainoverrides:
        d = etree.SubElement(unbound, "domainoverrides")
        sub(d, "domain", override.domain)
        sub(d, "ip", override.ip)
        if override.descr:
            sub(d, "descr", override.descr)
    if cfg.custom_options:
        sub(unbound, "custom_options", cfg.custom_options)
    return unbound
