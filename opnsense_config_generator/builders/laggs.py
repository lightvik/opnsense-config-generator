from lxml import etree

from opnsense_config_generator.models.laggs import LaggsConfig
from opnsense_config_generator.xml_utils import sub


def build_laggs(cfg: LaggsConfig) -> etree._Element | None:
    if not cfg.laggs:
        return None
    laggs = etree.Element("laggs")
    for lagg in cfg.laggs:
        l = etree.SubElement(laggs, "lagg")
        sub(l, "laggif", lagg.laggif)
        sub(l, "proto", lagg.proto)
        for member in lagg.members:
            sub(l, "members", member)
        for port in lagg.laggport:
            sub(l, "laggport", port)
        if lagg.descr:
            sub(l, "descr", lagg.descr)
    return laggs
