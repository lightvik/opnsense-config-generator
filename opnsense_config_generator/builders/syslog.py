from lxml import etree

from opnsense_config_generator.builders.base import bool_val
from opnsense_config_generator.models.syslog import SyslogConfig
from opnsense_config_generator.uuid_utils import make_uuid
from opnsense_config_generator.xml_utils import sub


def build_syslog(cfg: SyslogConfig) -> etree._Element:
    el = etree.Element("Syslog")

    gen = etree.SubElement(el, "general")
    sub(gen, "enabled", bool_val(cfg.general.enabled))
    sub(gen, "loglocal", bool_val(cfg.general.loglocal))
    sub(gen, "maxpreserve", str(cfg.general.maxpreserve))
    if cfg.general.maxfilesize is not None:
        sub(gen, "maxfilesize", str(cfg.general.maxfilesize))

    dests = etree.SubElement(el, "destinations")
    for dest in cfg.destinations:
        uid = make_uuid("syslog:destination", f"{dest.hostname}:{dest.port}")
        d = etree.SubElement(dests, "destination", uuid=uid)
        sub(d, "enabled", bool_val(dest.enabled))
        sub(d, "transport", dest.transport)
        if dest.program:
            sub(d, "program", ",".join(dest.program))
        if dest.level:
            sub(d, "level", ",".join(dest.level))
        if dest.facility:
            sub(d, "facility", ",".join(dest.facility))
        sub(d, "hostname", dest.hostname)
        if dest.certificate:
            sub(d, "certificate", dest.certificate)
        sub(d, "port", str(dest.port))
        sub(d, "rfc5424", bool_val(dest.rfc5424))
        sub(d, "description", dest.description)

    return el
