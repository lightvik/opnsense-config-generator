import uuid

from opnsense_config_generator.uuid_utils import NAMESPACE, make_uuid


def test_make_uuid_is_deterministic() -> None:
    assert make_uuid("filter", "rule1") == make_uuid("filter", "rule1")


def test_make_uuid_different_keys_differ() -> None:
    assert make_uuid("filter", "rule1") != make_uuid("filter", "rule2")
    assert make_uuid("filter", "rule1") != make_uuid("system", "rule1")


def test_make_uuid_is_valid_uuid() -> None:
    result = make_uuid("route", "10.0.0.0/8:GW_WAN")
    parsed = uuid.UUID(result)
    assert parsed.version == 5


def test_make_uuid_uses_namespace() -> None:
    expected = str(uuid.uuid5(NAMESPACE, "test:key"))
    assert make_uuid("test", "key") == expected
