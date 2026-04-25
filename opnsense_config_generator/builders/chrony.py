from lxml import etree

from opnsense_config_generator.builders.base import append_if, bool_val
from opnsense_config_generator.models.chrony import ChronyConfig
from opnsense_config_generator.xml_utils import sub


def build_chrony(cfg: ChronyConfig) -> etree._Element | None:
    if not cfg.general.enabled:
        return None

    el = etree.Element("chrony")
    gen = etree.SubElement(el, "general")

    sub(gen, "enabled", bool_val(cfg.general.enabled))
    sub(gen, "port", str(cfg.general.port))
    sub(gen, "ntsclient", bool_val(cfg.general.nts_client))
    sub(gen, "ntsnocert", bool_val(cfg.general.ntsnocert))
    sub(gen, "peers", ",".join(cfg.general.peers))
    append_if(gen, "fallbackpeers", cfg.general.fallback_peers or None)
    if cfg.general.allowed_networks:
        sub(gen, "allowednetworks", ",".join(cfg.general.allowed_networks))

    return el
