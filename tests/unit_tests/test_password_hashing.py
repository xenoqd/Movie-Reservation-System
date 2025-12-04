from backend.core.security.password import get_password_hash, verify_password


def test_get_different_hash():
    password = "strongpassword"

    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)

    assert hash1 != hash2

    assert hash1.startswith("$2b$")
    assert hash2.startswith("$2b$")


def test_verify_password_success():
    password = "StrongPassword123"
    hashed = get_password_hash(password)

    assert verify_password(password, hashed) is True


def test_verify_password_failure():
    password = "OriginalPassword"
    wrong_password = "WrongPassword"
    hashed = get_password_hash(password)

    assert verify_password(wrong_password, hashed) is False
