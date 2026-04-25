from lxml import etree

from opnsense_config_generator.models.routes import RoutesConfig
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub


def build_staticroutes(cfg: RoutesConfig) -> etree._Element | None:
    if not cfg.routes:
        return None
    staticroutes = etree.Element("staticroutes")
    for route in cfg.routes:
        r = etree.SubElement(staticroutes, "route")
        sub(r, "network", route.network)
        sub(r, "gateway", route.gateway)
        if route.descr:
            sub(r, "descr", route.descr)
        if route.disabled:
            sub(r, "disabled")
        sub(r, "uuid", make_uuid("route", f"{route.network}:{route.gateway}"))
    return staticroutes
