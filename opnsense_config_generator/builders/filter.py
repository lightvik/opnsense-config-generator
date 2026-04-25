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

    if rule.tag:
        sub(r, "tag", rule.tag)
    if rule.tagged:
        sub(r, "tagged", rule.tagged)

    tracker = rule.tracker or make_uuid("filter", f"{rule.interface}:{idx}:{rule.descr}")
    sub(r, "tracker", tracker)


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
