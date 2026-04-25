from lxml import etree


def make_root() -> etree._Element:
    return etree.Element("opnsense")


def serialize(root: etree._Element) -> bytes:
    """Serialize lxml tree to bytes matching OPNsense style (2-space indent, version="1.0")."""
    etree.indent(root, space="  ")
    return etree.tostring(
        root,
        xml_declaration=True,
        encoding="UTF-8",
        pretty_print=True,
    )


def sub(parent: etree._Element, tag: str, text: str | None = None) -> etree._Element:
    el = etree.SubElement(parent, tag)
    if text is not None:
        el.text = text
    return el
