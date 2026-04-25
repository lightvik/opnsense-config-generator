"""Golden tests: YAML input → compare against committed expected.xml."""

from pathlib import Path

import yaml
from lxml import etree

from opnsense_config_generator.build import build_xml
from opnsense_config_generator.models.root import OpnSenseConfig

GOLDEN_DIR = Path(__file__).parent / "golden"


def _get_golden_cases() -> list[Path]:
    return sorted(GOLDEN_DIR.glob("*/config.yaml"))


def _normalize_xml(xml_bytes: bytes) -> str:
    """Strip the <revision><time> element before comparing (it changes every run)."""
    root = etree.fromstring(xml_bytes)
    for rev in root.findall(".//revision/time"):
        rev.text = "TIMESTAMP"
    for pw in root.findall(".//password"):
        if pw.text and pw.text.startswith("$2"):
            pw.text = "BCRYPT_HASH"
    etree.indent(root, space="  ")
    return etree.tostring(root, pretty_print=True, encoding="unicode")


def _run_golden(case_name: str, update_snapshots: bool) -> None:
    case_dir = GOLDEN_DIR / case_name
    config_yaml = case_dir / "config.yaml"
    expected_xml = case_dir / "expected.xml"

    if not config_yaml.exists():
        return

    data = yaml.safe_load(config_yaml.read_text())
    cfg = OpnSenseConfig.model_validate(data)
    actual = _normalize_xml(build_xml(cfg))

    if update_snapshots or not expected_xml.exists():
        expected_xml.write_text(actual)
        return

    assert actual == expected_xml.read_text(), (
        f"Golden mismatch for {case_name}. "
        "Run with --update-snapshots to regenerate."
    )


def test_golden_minimal(update_snapshots: bool) -> None:
    _run_golden("minimal", update_snapshots)


def test_golden_typical(update_snapshots: bool) -> None:
    _run_golden("typical", update_snapshots)


def test_golden_full(update_snapshots: bool) -> None:
    _run_golden("full", update_snapshots)
