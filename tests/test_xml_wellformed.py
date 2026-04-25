from pathlib import Path

import yaml
from lxml import etree

from opnsense_config_generator.build import build_xml
from opnsense_config_generator.models.root import OpnSenseConfig
from opnsense_config_generator.version import OPNSENSE_VERSION

MINIMAL_YAML = Path(__file__).parent / "golden/minimal/config.yaml"


def test_xml_is_wellformed() -> None:
    data = yaml.safe_load(MINIMAL_YAML.read_text())
    cfg = OpnSenseConfig.model_validate(data)
    xml_bytes = build_xml(cfg)
    root = etree.fromstring(xml_bytes)
    assert root is not None


def test_xml_root_is_opnsense() -> None:
    data = yaml.safe_load(MINIMAL_YAML.read_text())
    cfg = OpnSenseConfig.model_validate(data)
    xml_bytes = build_xml(cfg)
    root = etree.fromstring(xml_bytes)
    assert root.tag == "opnsense"


def test_xml_version_matches_constant() -> None:
    data = yaml.safe_load(MINIMAL_YAML.read_text())
    cfg = OpnSenseConfig.model_validate(data)
    xml_bytes = build_xml(cfg)
    root = etree.fromstring(xml_bytes)
    version_el = root.find("version")
    assert version_el is not None
    assert version_el.text == OPNSENSE_VERSION


def test_xml_has_required_sections() -> None:
    data = yaml.safe_load(MINIMAL_YAML.read_text())
    cfg = OpnSenseConfig.model_validate(data)
    xml_bytes = build_xml(cfg)
    root = etree.fromstring(xml_bytes)
    required = {"system", "interfaces", "filter", "nat", "unbound"}
    present = {child.tag for child in root}
    assert required <= present


def test_xml_password_is_bcrypt() -> None:
    data = yaml.safe_load(MINIMAL_YAML.read_text())
    cfg = OpnSenseConfig.model_validate(data)
    xml_bytes = build_xml(cfg)
    root = etree.fromstring(xml_bytes)
    for pw in root.findall(".//password"):
        assert pw.text is not None
        assert pw.text.startswith("$2"), f"Plaintext password found: {pw.text}"
