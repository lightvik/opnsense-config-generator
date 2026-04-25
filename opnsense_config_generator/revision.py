import time

from lxml import etree

from opnsense_config_generator.version import OPNSENSE_VERSION, TOOL_VERSION


def build_revision_block() -> etree._Element:
    revision = etree.Element("revision")

    username = etree.SubElement(revision, "username")
    username.text = "opnsense-config-generator"

    timestamp = etree.SubElement(revision, "time")
    timestamp.text = str(int(time.time()))

    description = etree.SubElement(revision, "description")
    description.text = (
        f"Imported by opnsense-config-generator v{TOOL_VERSION} (OPNsense {OPNSENSE_VERSION})"
    )

    return revision
