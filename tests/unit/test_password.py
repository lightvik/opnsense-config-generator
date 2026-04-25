import bcrypt

from opnsense_config_generator.password import hash_password


def test_hash_is_bcrypt() -> None:
    h = hash_password("secret")
    assert h.startswith("$2b$")


def test_hash_validates() -> None:
    h = hash_password("mysecret")
    assert bcrypt.checkpw(b"mysecret", h.encode())


def test_hash_is_not_plaintext() -> None:
    assert hash_password("plaintext") != "plaintext"


def test_each_hash_is_different() -> None:
    # bcrypt uses random salt
    assert hash_password("same") != hash_password("same")
