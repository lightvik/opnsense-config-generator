from lxml import etree

from opnsense_config_generator.models.vlans import VlansConfig
from opnsense_config_generator.xml_utils import sub


def build_vlans(cfg: VlansConfig) -> etree._Element | None:
    if not cfg.vlans:
        return None
    vlans = etree.Element("vlans")
    for vlan in cfg.vlans:
        v = etree.SubElement(vlans, "vlan")
        sub(v, "if", vlan.if_name)
        sub(v, "tag", str(vlan.tag))
        sub(v, "pcp", str(vlan.pcp))
        if vlan.descr:
            sub(v, "descr", vlan.descr)
        if vlan.vlanif:
            sub(v, "vlanif", vlan.vlanif)
    return vlans
