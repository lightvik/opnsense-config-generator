from lxml import etree

from opnsense_config_generator.models.nat import NatAddress, NatConfig, OutboundNatRule, PortForward
from opnsense_config_generator.xml_utils import sub


def build_nat(cfg: NatConfig) -> etree._Element:
    nat = etree.Element("nat")

    outbound = etree.SubElement(nat, "outbound")
    sub(outbound, "mode", cfg.outbound_mode)
    for outbound_rule in cfg.outbound_rules:
        _build_outbound_rule(outbound, outbound_rule)

    for pf in cfg.port_forwards:
        _build_port_forward(nat, pf)

    for o2o in cfg.one_to_one:
        one = etree.SubElement(nat, "onetoone")
        sub(one, "interface", o2o.interface)
        _build_nat_address(one, "source", o2o.source)
        _build_nat_address(one, "destination", o2o.destination)
        sub(one, "target", o2o.target)
        if o2o.descr:
            sub(one, "descr", o2o.descr)
        if o2o.disabled:
            sub(one, "disabled")

    return nat


def _build_outbound_rule(parent: etree._Element, rule: OutboundNatRule) -> None:
    r = etree.SubElement(parent, "rule")
    sub(r, "interface", rule.interface)
    sub(r, "ipprotocol", rule.ipprotocol)
    if rule.protocol:
        sub(r, "protocol", rule.protocol)
    _build_nat_address(r, "source", rule.source)
    if rule.sourceport:
        sub(r, "sourceport", rule.sourceport)
    _build_nat_address(r, "destination", rule.destination)
    if rule.dstport:
        sub(r, "dstport", rule.dstport)
    if rule.target:
        sub(r, "target", rule.target)
    if rule.natport:
        sub(r, "natport", rule.natport)
    if rule.descr:
        sub(r, "descr", rule.descr)
    if rule.disabled:
        sub(r, "disabled")
    if rule.nonat:
        sub(r, "nonat")
    if rule.staticnatport:
        sub(r, "staticnatport")
    if rule.poolopts:
        sub(r, "poolopts", rule.poolopts)
    if rule.poolopts_sourcehashkey:
        sub(r, "poolopts_sourcehashkey", rule.poolopts_sourcehashkey)
    if rule.log:
        sub(r, "log")
    if rule.nosync:
        sub(r, "nosync")
    if rule.tag:
        sub(r, "tag", rule.tag)
    if rule.tagged:
        sub(r, "tagged", rule.tagged)
    if rule.category:
        sub(r, "category", rule.category)


def _build_port_forward(parent: etree._Element, rule: PortForward) -> None:
    r = etree.SubElement(parent, "rule")
    if rule.sequence is not None:
        sub(r, "sequence", str(rule.sequence))
    sub(r, "interface", rule.interface)
    sub(r, "ipprotocol", rule.ipprotocol)
    sub(r, "protocol", rule.protocol)
    _build_nat_address(r, "source", rule.source)
    _build_nat_address(r, "destination", rule.destination)
    sub(r, "target", rule.target)
    if rule.local_port:
        sub(r, "local-port", rule.local_port)
    if rule.descr:
        sub(r, "descr", rule.descr)
    if rule.disabled:
        sub(r, "disabled")
    if rule.nordr:
        sub(r, "nordr")
    if rule.log:
        sub(r, "log")
    if rule.poolopts:
        sub(r, "poolopts", rule.poolopts)
    if rule.tag:
        sub(r, "tag", rule.tag)
    if rule.tagged:
        sub(r, "tagged", rule.tagged)
    if rule.nosync:
        sub(r, "nosync")
    if rule.natreflection:
        sub(r, "natreflection", rule.natreflection)
    if rule.pass_rule:
        sub(r, "pass", rule.pass_rule)
    if rule.category:
        sub(r, "category", rule.category)
    sub(r, "associated-rule-id", rule.associated_rule_id)


def _build_nat_address(parent: etree._Element, tag: str, addr: NatAddress) -> None:
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
