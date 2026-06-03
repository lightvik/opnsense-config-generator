from lxml import etree

from opnsense_config_generator.models.filter import FilterConfig, FilterRule, RuleAddress
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub


def build_filter(cfg: FilterConfig) -> etree._Element:
    filter_el = etree.Element("filter")
    for i, rule in enumerate(cfg.rules):
        _build_rule(filter_el, rule, i)
    return filter_el


def _build_rule(parent: etree._Element, rule: FilterRule, idx: int) -> None:
    r = etree.SubElement(parent, "rule")
    sub(r, "type", rule.type)
    sub(r, "ipprotocol", rule.ipprotocol)
    if rule.descr:
        sub(r, "descr", rule.descr)
    if rule.disabled:
        sub(r, "disabled")
    if rule.log:
        sub(r, "log")
    sub(r, "interface", rule.interface)
    if rule.direction:
        sub(r, "direction", rule.direction)
    if rule.protocol:
        sub(r, "protocol", rule.protocol)
    if rule.statetype:
        sub(r, "statetype", rule.statetype)
    if rule.quick:
        sub(r, "quick")
    if rule.floating:
        sub(r, "floating", "yes")

    _build_address(r, "source", rule.source)
    _build_address(r, "destination", rule.destination)

    if rule.icmptype:
        sub(r, "icmptype", ",".join(rule.icmptype))
    if rule.icmp6type:
        sub(r, "icmp6-type", ",".join(rule.icmp6type))
    if rule.gateway:
        sub(r, "gateway", rule.gateway)
    if rule.reply_to:
        sub(r, "reply-to", rule.reply_to)
    if rule.disablereplyto:
        sub(r, "disablereplyto")
    if rule.sched:
        sub(r, "sched", rule.sched)
    if rule.shaper1:
        sub(r, "shaper1", rule.shaper1)
    if rule.shaper2:
        sub(r, "shaper2", rule.shaper2)
    if rule.set_prio:
        sub(r, "set-prio", rule.set_prio)
    if rule.set_prio_low:
        sub(r, "set-prio-low", rule.set_prio_low)
    if rule.prio:
        sub(r, "prio", rule.prio)
    if rule.tos:
        sub(r, "tos", rule.tos)
    if rule.tcpflags1:
        sub(r, "tcpflags1", rule.tcpflags1)
    if rule.tcpflags2:
        sub(r, "tcpflags2", rule.tcpflags2)
    if rule.tcpflags_any:
        sub(r, "tcpflags_any")
    if rule.allowopts:
        sub(r, "allowopts")
    if rule.overload:
        sub(r, "overload", rule.overload)
    if rule.statetimeout:
        sub(r, "statetimeout", rule.statetimeout)
    if rule.max_src_conn_rate:
        sub(r, "max-src-conn-rate", rule.max_src_conn_rate)
    if rule.max_src_conn_rates:
        sub(r, "max-src-conn-rates", rule.max_src_conn_rates)
    if rule.tag:
        sub(r, "tag", rule.tag)
    if rule.tagged:
        sub(r, "tagged", rule.tagged)
    if rule.nosync:
        sub(r, "nosync")
    if rule.nopfsync:
        sub(r, "nopfsync")
    if rule.categories:
        sub(r, "categories", rule.categories)
    if rule.divert_to:
        sub(r, "divert-to", rule.divert_to)
    if rule.state_policy:
        sub(r, "state-policy", rule.state_policy)
    if rule.os:
        sub(r, "os", rule.os)
    if rule.max:
        sub(r, "max", rule.max)
    if rule.max_src_nodes:
        sub(r, "max-src-nodes", rule.max_src_nodes)
    if rule.max_src_conn:
        sub(r, "max-src-conn", rule.max_src_conn)
    if rule.max_src_states:
        sub(r, "max-src-states", rule.max_src_states)

    tracker = rule.tracker or make_uuid("filter", f"{rule.interface}:{idx}:{rule.descr}")
    sub(r, "tracker", tracker)
    if rule.associated_rule_id:
        sub(r, "associated-rule-id", rule.associated_rule_id)


def _build_address(parent: etree._Element, tag: str, addr: RuleAddress) -> None:
    el = etree.SubElement(parent, tag)
    if addr.any:
        etree.SubElement(el, "any")
    elif addr.network:
        invert = "!" if addr.invert else ""
        sub(el, "network", f"{invert}{addr.network}")
    elif addr.address:
        invert = "!" if addr.invert else ""
        sub(el, "address", f"{invert}{addr.address}")
    if addr.port:
        sub(el, "port", addr.port)
