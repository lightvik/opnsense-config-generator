from lxml import etree

from opnsense_config_generator.builders.base import append_if, bool_val
from opnsense_config_generator.models.git_backup import GitBackupConfig
from opnsense_config_generator.xml_utils import sub


def build_git_backup(cfg: GitBackupConfig) -> etree._Element | None:
    if not cfg.enabled:
        return None

    el = etree.Element("git")
    sub(el, "enabled", bool_val(cfg.enabled))
    append_if(el, "url", cfg.url or None)
    sub(el, "branch", cfg.branch)
    sub(el, "force_push", bool_val(cfg.force_push))
    append_if(el, "privkey", cfg.privkey or None)
    append_if(el, "user", cfg.user or None)
    append_if(el, "password", cfg.password or None)

    return el
