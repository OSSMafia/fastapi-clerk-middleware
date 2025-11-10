from time import time

import jwt
import pytest


@pytest.fixture
def jwt_token():
    return generate_jwt()


def generate_jwt():
    with open("./mock_files/test_private_key.pem") as key_file:
        private_key = key_file.read()

    payload = {"sub": "1234567890", "iat": int(time()), "exp": int(time()) + 300}

    return jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": "ins_test_key_1"})
