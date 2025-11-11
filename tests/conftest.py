from time import time

import jwt
import pytest


def generate_jwt(payload: dict) -> str:
    with open("./mock_files/test_private_key.pem") as key_file:
        private_key = key_file.read()

    return jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": "ins_test_key_1"})


@pytest.fixture
def jwt_token_default():
    payload = {
        "sub": "1234567890",
        "iat": int(time()),
        "exp": int(time()) + 300,
    }
    return generate_jwt(payload)


@pytest.fixture
def jwt_token_audience():
    payload = {
        "sub": "1234567890",
        "aud": "test",
        "iat": int(time()),
        "exp": int(time()) + 300,
    }
    return generate_jwt(payload)


@pytest.fixture
def jwt_token_issuer():
    payload = {
        "sub": "1234567890",
        "iat": int(time()),
        "exp": int(time()) + 300,
        "iss": "test_issuer",
    }
    return generate_jwt(payload)


@pytest.fixture
def jwt_token_iat_future():
    payload = {
        "sub": "1234567890",
        "iat": int(time()) + 600,
        "exp": int(time()) + 900,
    }
    return generate_jwt(payload)


@pytest.fixture
def jwt_token_iat_future_short_leeway():
    payload = {
        "sub": "1234567890",
        "iat": int(time()) + 10,
        "exp": int(time()) + 600,
    }
    return generate_jwt(payload)


@pytest.fixture
def jwt_token_expired():
    payload = {
        "sub": "1234567890",
        "iat": int(time()),
        "exp": int(time()) - 300,
    }
    return generate_jwt(payload)
