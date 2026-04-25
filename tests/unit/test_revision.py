from opnsense_config_generator.revision import build_revision_block
from opnsense_config_generator.version import OPNSENSE_VERSION, TOOL_VERSION


def test_revision_has_required_children() -> None:
    rev = build_revision_block()
    tags = {child.tag for child in rev}
    assert {"username", "time", "description"} <= tags


def test_revision_username() -> None:
    rev = build_revision_block()
    username = rev.find("username")
    assert username is not None
    assert username.text == "opnsense-config-generator"


def test_revision_description_contains_versions() -> None:
    rev = build_revision_block()
    desc = rev.find("description")
    assert desc is not None and desc.text is not None
    assert TOOL_VERSION in desc.text
    assert OPNSENSE_VERSION in desc.text


def test_revision_time_is_numeric() -> None:
    rev = build_revision_block()
    time_el = rev.find("time")
    assert time_el is not None and time_el.text is not None
    int(time_el.text)  # must not raise
