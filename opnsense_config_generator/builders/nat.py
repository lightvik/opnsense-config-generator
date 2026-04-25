from lxml import etree

from opnsense_config_generator.models.nat import NatAddress, NatConfig, OutboundNatRule, PortForward
from opnsense_config_generator.xml_utils import sub


def build_nat(cfg: NatConfig) -> etree._Element:
    nat = etree.Element("nat")

    outbound = etree.SubElement(nat, "outbound")
    sub(outbound, "mode", cfg.outbound_mode)
    for rule in cfg.outbound_rules:
        _build_outbound_rule(outbound, rule)

    for rule in cfg.port_forwards:
        _build_port_forward(nat, rule)

    for rule in cfg.one_to_one:
        one = etree.SubElement(nat, "onetoone")
        sub(one, "interface", rule.interface)
        _build_nat_address(one, "source", rule.source)
        _build_nat_address(one, "destination", rule.destination)
        sub(one, "target", rule.target)
        if rule.descr:
            sub(one, "descr", rule.descr)
        if rule.disabled:
            sub(one, "disabled")

    return nat


def _build_outbound_rule(parent: etree._Element, rule: OutboundNatRule) -> None:
    r = etree.SubElement(parent, "rule")
    sub(r, "interface", rule.interface)
    _build_nat_address(r, "source", rule.source)
    _build_nat_address(r, "destination", rule.destination)
    if rule.target:
        sub(r, "target", rule.target)
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


def _build_port_forward(parent: etree._Element, rule: PortForward) -> None:
    r = etree.SubElement(parent, "rule")
    sub(r, "interface", rule.interface)
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
    sub(r, "associated-rule-id", rule.associated_rule_id)


def _build_nat_address(parent: etree._Element, tag: str, addr: NatAddress) -> None:
    el = etree.SubElement(parent, tag)
    if addr.any:
        etree.SubElement(el, "any")
    elif addr.network:
        sub(el, "network", addr.network)
    elif addr.address:
        sub(el, "address", addr.address)
    if addr.port:
        sub(el, "port", addr.port)
