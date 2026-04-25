from lxml import etree

from opnsense_config_generator.models.ntpd import NtpdConfig
from opnsense_config_generator.xml_utils import sub


def build_ntpd(cfg: NtpdConfig) -> etree._Element | None:
    if not cfg.servers:
        return None

    el = etree.Element("ntpd")

    prefer = [s.address for s in cfg.servers if s.prefer]
    pool = [s.address for s in cfg.servers if s.pool]
    noselect = [s.address for s in cfg.servers if s.noselect]

    if prefer:
        sub(el, "prefer", " ".join(prefer))
    if pool:
        sub(el, "ispool", " ".join(pool))
    if noselect:
        sub(el, "noselect", " ".join(noselect))
    if cfg.interface:
        sub(el, "interface", cfg.interface)
    if cfg.orphan != 12:
        sub(el, "orphan", str(cfg.orphan))

    return el
