from lxml import etree

from opnsense_config_generator.models.aliases import AliasesConfig
from opnsense_config_generator.xml_utils import sub


def build_aliases(cfg: AliasesConfig) -> etree._Element | None:
    if not cfg.aliases:
        return None
    aliases = etree.Element("aliases")
    for alias in cfg.aliases:
        a = etree.SubElement(aliases, "alias")
        sub(a, "name", alias.name)
        sub(a, "type", alias.type)
        if alias.descr:
            sub(a, "descr", alias.descr)
        sub(a, "content", "\n".join(alias.content))
        sub(a, "enabled", "1" if alias.enabled else "0")
        if alias.proto:
            sub(a, "proto", alias.proto)
        if alias.updatefreq:
            sub(a, "updatefreq", str(alias.updatefreq))
        if alias.counters:
            sub(a, "counters", "1")
        if alias.interface:
            sub(a, "interface", alias.interface)
    return aliases
