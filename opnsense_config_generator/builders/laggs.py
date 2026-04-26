from lxml import etree

from opnsense_config_generator.models.laggs import LaggsConfig
from opnsense_config_generator.xml_utils import sub


def build_laggs(cfg: LaggsConfig) -> etree._Element | None:
    if not cfg.laggs:
        return None
    laggs = etree.Element("laggs")
    for lagg in cfg.laggs:
        el = etree.SubElement(laggs, "lagg")
        sub(el, "laggif", lagg.laggif)
        sub(el, "proto", lagg.proto)
        for member in lagg.members:
            sub(el, "members", member)
        for port in lagg.laggport:
            sub(el, "laggport", port)
        if lagg.descr:
            sub(el, "descr", lagg.descr)
    return laggs
