from lxml import etree

from opnsense_config_generator.builders.base import bool_val
from opnsense_config_generator.models.qemu_guest_agent import QemuGuestAgentConfig
from opnsense_config_generator.xml_utils import sub


def build_qemu_guest_agent(cfg: QemuGuestAgentConfig) -> etree._Element | None:
    if not cfg.enabled:
        return None

    el = etree.Element("QemuGuestAgent")
    gen = etree.SubElement(el, "general")
    sub(gen, "Enabled", bool_val(cfg.enabled))
    sub(gen, "LogDebug", bool_val(cfg.log_debug))
    if cfg.disabled_rpcs:
        sub(gen, "DisabledRPCs", ",".join(cfg.disabled_rpcs))

    return el
