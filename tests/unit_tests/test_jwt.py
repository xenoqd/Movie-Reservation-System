import pytest
from datetime import timedelta, datetime


from fastapi import HTTPException
from backend.core.config import settings
from backend.core.security.jwt import create_access_token, decode_access_token

SECRET_KEY = settings.SECRET_KEY
# REFRESH_SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
# REFRESH_TOKEN_EXPIRE_DAYS = 7


def test_create_access_token_contains_sub():
    data = {"sub": "5"}
    token = create_access_token(data=data)

    payload = decode_access_token(token)

    assert payload["sub"] == "5"


def test_create_access_token_has_exp_claim():
    data = {"sub": "5"}
    token = create_access_token(data=data)

    payload = decode_access_token(token)

    assert "exp" in payload
    assert payload["exp"] > datetime.utcnow().timestamp()


def test_create_access_token_custom_expiration():
    data = {"sub": "10"}
    expires = timedelta(minutes=1)

    token = create_access_token(data=data, expires_delta=expires)
    payload = decode_access_token(token)

    exp = payload["exp"]
    assert exp > datetime.utcnow().timestamp()


def test_decode_access_token_invalid_signature():
    data = {"sub": "100"}
    token = create_access_token(data=data)

    invalid_token = token[:-1] + ("A" if token[-1] != "A" else "B")

    with pytest.raises(HTTPException) as exc:
        decode_access_token(invalid_token)

    assert exc.value.status_code == 401
    assert "Invalid token" in exc.value.detail


def test_decode_access_token_expired():
    data = {"sub": "123"}
    expired_delta = timedelta(seconds=-5)

    token = create_access_token(data=data, expires_delta=expired_delta)

    with pytest.raises(HTTPException) as exc:
        decode_access_token(token)

    assert exc.value.status_code == 401
    assert "Invalid token" in exc.value.detail
