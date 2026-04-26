from lxml import etree

from opnsense_config_generator.xml_utils import sub


def bool_val(value: bool) -> str:
    return "1" if value else "0"


def append_if(parent: etree._Element, tag: str, value: str | int | bool | None) -> None:
    """Append element only when value is non-empty / non-None."""
    if value is None:
        return
    text = bool_val(value) if isinstance(value, bool) else str(value)
    if text:
        sub(parent, tag, text)
