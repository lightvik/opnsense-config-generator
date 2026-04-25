from lxml import etree

from opnsense_config_generator.models.bridges import BridgesConfig
from opnsense_config_generator.xml_utils import sub


def build_bridges(cfg: BridgesConfig) -> etree._Element | None:
    if not cfg.bridges:
        return None
    bridges = etree.Element("bridges")
    for bridge in cfg.bridges:
        b = etree.SubElement(bridges, "bridged")
        sub(b, "bridgeif", bridge.bridgeif)
        for member in bridge.members:
            sub(b, "member", member)
        if bridge.descr:
            sub(b, "descr", bridge.descr)
        if bridge.stp:
            sub(b, "stp", " ".join(bridge.members))
        if bridge.rstp:
            sub(b, "rstp", " ".join(bridge.members))
        sub(b, "maxaddr", str(bridge.maxaddr))
        sub(b, "timeout", str(bridge.timeout))
    return bridges
