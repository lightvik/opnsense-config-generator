from lxml import etree

from opnsense_config_generator.models.unbound import UnboundConfig
from opnsense_config_generator.xml_utils import sub


def build_unbound(cfg: UnboundConfig) -> etree._Element:
    unbound = etree.Element("unbound")
    if cfg.enable:
        sub(unbound, "enable", "1")
    if cfg.port:
        sub(unbound, "port", cfg.port)
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
    if cfg.dns64prefix:
        sub(unbound, "dns64prefix", cfg.dns64prefix)
    if cfg.log_queries:
        sub(unbound, "log_verbosity", "2")
    if cfg.logverbosity and not cfg.log_queries:
        sub(unbound, "log_verbosity", cfg.logverbosity)
    if cfg.logqueries:
        sub(unbound, "logqueries")
    if cfg.logreplies:
        sub(unbound, "logreplies")
    if cfg.logtagqueryreply:
        sub(unbound, "logtagqueryreply")
    if cfg.loglocal:
        sub(unbound, "loglocal")
    if cfg.extendedstatistics:
        sub(unbound, "extendedstatistics")
    if cfg.stats:
        sub(unbound, "stats")
    if cfg.cache_max_ttl != 86400:
        sub(unbound, "cache_max_ttl", str(cfg.cache_max_ttl))
    if cfg.cache_min_ttl:
        sub(unbound, "cache_min_ttl", str(cfg.cache_min_ttl))
    if cfg.msgcachesize is not None:
        sub(unbound, "msgcachesize", str(cfg.msgcachesize))
    if cfg.rrsetcachesize is not None:
        sub(unbound, "rrsetcachesize", str(cfg.rrsetcachesize))
    if cfg.outgoingnumtcp is not None:
        sub(unbound, "outgoingnumtcp", str(cfg.outgoingnumtcp))
    if cfg.incomingnumtcp is not None:
        sub(unbound, "incomingnumtcp", str(cfg.incomingnumtcp))
    if cfg.numqueriesperthread is not None:
        sub(unbound, "numqueriesperthread", str(cfg.numqueriesperthread))
    if cfg.jostle_timeout is not None:
        sub(unbound, "jostle_timeout", str(cfg.jostle_timeout))
    if cfg.noarecords:
        sub(unbound, "noarecords")
    if cfg.txtsupport:
        sub(unbound, "txtsupport")
    if cfg.safesearch:
        sub(unbound, "safesearch")
    if cfg.local_zone_type:
        sub(unbound, "local_zone_type", cfg.local_zone_type)
    if cfg.enable_wpad:
        sub(unbound, "enable_wpad")
    if cfg.dnssecstripped:
        sub(unbound, "dnssecstripped")
    if cfg.belownxdomain:
        sub(unbound, "belownxdomain")
    if cfg.aggressivensec:
        sub(unbound, "aggressivensec")
    if cfg.serveexpired:
        sub(unbound, "serveexpired")
    if cfg.serveexpiredttl is not None:
        sub(unbound, "serveexpiredttl", str(cfg.serveexpiredttl))
    if cfg.serveexpiredttlreset:
        sub(unbound, "serveexpiredttlreset")
    if cfg.serveexpiredclienttimeout is not None:
        sub(unbound, "serveexpiredclienttimeout", str(cfg.serveexpiredclienttimeout))
    if cfg.qnameminstrict:
        sub(unbound, "qnameminstrict")
    if cfg.regdhcp:
        sub(unbound, "regdhcp")
    if cfg.regdhcpdomain:
        sub(unbound, "regdhcpdomain", cfg.regdhcpdomain)
    if cfg.regdhcpstatic:
        sub(unbound, "regdhcpstatic")
    if cfg.noreglladdr6:
        sub(unbound, "noreglladdr6")
    for server in cfg.forward_servers:
        sub(unbound, "forwarder", server)
    for domain in cfg.privatedomain:
        sub(unbound, "privatedomain", domain)
    for addr in cfg.privateaddress:
        sub(unbound, "privateaddress", addr)
    for domain in cfg.insecuredomain:
        sub(unbound, "insecuredomain", domain)
    for host in cfg.hosts:
        h = etree.SubElement(unbound, "hosts")
        sub(h, "host", host.host)
        sub(h, "domain", host.domain)
        sub(h, "ip", host.ip)
        if host.descr:
            sub(h, "descr", host.descr)
        if host.rr:
            sub(h, "rr", host.rr)
        if host.mxprio:
            sub(h, "mxprio", host.mxprio)
        if host.ttl:
            sub(h, "ttl", host.ttl)
        if host.txtdata:
            sub(h, "txtdata", host.txtdata)
        if host.addptr:
            sub(h, "addptr")
        for alias in host.alias:
            a = etree.SubElement(h, "alias")
            sub(a, "host", alias.host)
            sub(a, "domain", alias.domain)
            if alias.descr:
                sub(a, "descr", alias.descr)
        for legacy_alias in host.aliases:
            sub(h, "aliases", legacy_alias)
    for override in cfg.domainoverrides:
        d = etree.SubElement(unbound, "domainoverrides")
        sub(d, "domain", override.domain)
        sub(d, "ip", override.ip)
        if override.descr:
            sub(d, "descr", override.descr)
    for acl in cfg.acls:
        a = etree.SubElement(unbound, "acls")
        sub(a, "aclname", acl.aclname)
        sub(a, "aclaction", acl.aclaction)
        if acl.description:
            sub(a, "description", acl.description)
        for net in acl.networks:
            sub(a, "row", net)
    for dot in cfg.dots:
        d = etree.SubElement(unbound, "dots")
        sub(d, "server", dot.server)
        sub(d, "port", dot.port)
        if dot.verify:
            sub(d, "verify", dot.verify)
    if cfg.custom_options:
        sub(unbound, "custom_options", cfg.custom_options)
    return unbound
