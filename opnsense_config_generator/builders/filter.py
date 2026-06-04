import ipaddress
import re as _re

from lxml import etree

from opnsense_config_generator.builders.base import append_if
from opnsense_config_generator.models.filter import FilterConfig, FilterRule, RuleAddress
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub

_STATETYPE_MAP = {
    "keep state": "keep",
    "synproxy state": "synproxy",
    "sloppy state": "sloppy",
    "modulate state": "modulate",
    "none": "none",
}


def build_filter(cfg: FilterConfig) -> etree._Element:
    firewall_el = etree.Element("Firewall")
    filter_el = etree.SubElement(firewall_el, "Filter")
    filter_el.set("version", "1.0.4")
    filter_el.set("description", "Firewall rules (new)")

    rules_el = etree.SubElement(filter_el, "rules")
    for i, rule in enumerate(cfg.rules):
        _build_rule(rules_el, rule, i)

    etree.SubElement(filter_el, "snatrules")
    etree.SubElement(filter_el, "npt")
    etree.SubElement(filter_el, "onetoone")

    return firewall_el


_IFACE_NAME_RE = _re.compile(r"^[a-z][a-z0-9]*$")


def _is_interface_name(s: str) -> bool:
    """Return True if s is an interface name (wan/lan/opt1…), not an IP or named alias."""
    try:
        ipaddress.ip_address(s)
        return False
    except ValueError:
        pass
    try:
        ipaddress.ip_network(s, strict=False)
        return False
    except ValueError:
        pass
    return bool(_IFACE_NAME_RE.match(s))


def _resolve_net(addr: RuleAddress) -> str:
    if addr.any:
        return "any"
    if addr.network:
        return addr.network
    if addr.address:
        if _is_interface_name(addr.address):
            return addr.address + "ip"
        return addr.address
    return "any"


def _build_rule(parent: etree._Element, rule: FilterRule, idx: int) -> None:
    uuid = rule.tracker or make_uuid("filter", f"{rule.interface}:{idx}:{rule.descr}")
    r = etree.SubElement(parent, "rule")
    r.set("uuid", uuid)

    sub(r, "enabled", "0" if rule.disabled else "1")
    sub(r, "sequence", str((idx + 1) * 10))
    sub(r, "action", rule.type)
    sub(r, "quick", "1" if rule.quick else "0")
    sub(r, "interface", rule.interface)
    sub(r, "direction", rule.direction or "in")
    sub(r, "ipprotocol", rule.ipprotocol)
    sub(r, "protocol", rule.protocol or "any")

    sub(r, "source_net", _resolve_net(rule.source))
    sub(r, "source_not", "1" if rule.source.invert else "0")
    append_if(r, "source_port", rule.source.port)

    sub(r, "destination_net", _resolve_net(rule.destination))
    sub(r, "destination_not", "1" if rule.destination.invert else "0")
    append_if(r, "destination_port", rule.destination.port)

    sub(r, "log", "1" if rule.log else "0")
    append_if(r, "description", rule.descr)

    if rule.statetype:
        append_if(r, "statetype", _STATETYPE_MAP.get(rule.statetype, rule.statetype))

    append_if(r, "state-policy", rule.state_policy)
    append_if(r, "gateway", rule.gateway)
    append_if(r, "replyto", rule.reply_to)
    if rule.disablereplyto:
        sub(r, "disablereplyto", "1")

    if rule.icmptype:
        sub(r, "icmptype", ",".join(rule.icmptype))
    if rule.icmp6type:
        sub(r, "icmp6type", ",".join(rule.icmp6type))

    if rule.tcpflags1:
        sub(r, "tcpflags1", rule.tcpflags1)
    if rule.tcpflags2:
        sub(r, "tcpflags2", rule.tcpflags2)
    if rule.tcpflags_any:
        sub(r, "tcpflags_any", "1")

    if rule.allowopts:
        sub(r, "allowopts", "1")
    if rule.nosync:
        sub(r, "nosync", "1")
    if rule.nopfsync:
        sub(r, "nopfsync", "1")

    append_if(r, "max", rule.max)
    append_if(r, "max-src-nodes", rule.max_src_nodes)
    append_if(r, "max-src-conn", rule.max_src_conn)
    append_if(r, "max-src-states", rule.max_src_states)
    append_if(r, "max-src-conn-rate", rule.max_src_conn_rate)
    append_if(r, "max-src-conn-rates", rule.max_src_conn_rates)
    append_if(r, "overload", rule.overload)
    append_if(r, "statetimeout", rule.statetimeout)
    append_if(r, "tag", rule.tag)
    append_if(r, "tagged", rule.tagged)
    append_if(r, "prio", rule.prio)
    append_if(r, "set-prio", rule.set_prio)
    append_if(r, "set-prio-low", rule.set_prio_low)
    append_if(r, "tos", rule.tos)
    append_if(r, "shaper1", rule.shaper1)
    append_if(r, "shaper2", rule.shaper2)
    append_if(r, "sched", rule.sched)
    append_if(r, "categories", rule.categories)
    append_if(r, "divert-to", rule.divert_to)
