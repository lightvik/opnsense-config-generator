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
    iburst = [s.address for s in cfg.servers if s.iburst]

    if prefer:
        sub(el, "prefer", " ".join(prefer))
    if pool:
        sub(el, "ispool", " ".join(pool))
    if noselect:
        sub(el, "noselect", " ".join(noselect))
    if iburst:
        sub(el, "iburst", " ".join(iburst))
    if cfg.interface:
        sub(el, "interface", cfg.interface)
    if cfg.orphan != 12:
        sub(el, "orphan", str(cfg.orphan))
    if cfg.maxclock is not None:
        sub(el, "maxclock", str(cfg.maxclock))
    if cfg.clientmode:
        sub(el, "clientmode")
    if cfg.clockstats:
        sub(el, "clockstats")
    if cfg.kod:
        sub(el, "kod")
    if cfg.limited:
        sub(el, "limited")
    if cfg.nomodify:
        sub(el, "nomodify")
    if cfg.nopeer:
        sub(el, "nopeer")
    if cfg.noserve:
        sub(el, "noserve")
    if cfg.notrap:
        sub(el, "notrap")
    if cfg.query:
        sub(el, "query")
    if cfg.logpeer:
        sub(el, "logpeer")
    if cfg.logsys:
        sub(el, "logsys")
    if cfg.loopstats:
        sub(el, "loopstats")
    if cfg.peerstats:
        sub(el, "peerstats")
    if cfg.statsgraph:
        sub(el, "statsgraph")
    if cfg.leapsec:
        sub(el, "leapsec", cfg.leapsec)
    if cfg.custom_options:
        sub(el, "custom_options", cfg.custom_options)

    return el
