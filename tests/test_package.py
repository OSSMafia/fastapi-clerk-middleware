import requests

API_SERVER_URL = "http://mock_api_server:8001"
JWKS_SERVER_URL = "http://mock_jwks_server:8000/.well-known/jwks.json"


def test_jwks_endpoint():
    """
    Test that the JWKS endpoint is reachable and returns keys.
    """
    response = requests.get(JWKS_SERVER_URL)
    assert response.status_code == 200
    jwks = response.json()
    assert "keys" in jwks


def test_default_denied():
    """
    Test that access to the protected route is denied without a token.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/default")
    assert response.status_code == 403


def test_default_denied_expired(jwt_token_expired):
    """
    Test that access to the protected route is denied with an expired JWT token.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/default", headers={"Authorization": f"Bearer {jwt_token_expired}"})
    assert response.status_code == 403


def test_default_success(jwt_token_default):
    """
    Test that access to the protected route is granted with a valid JWT token.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/default", headers={"Authorization": f"Bearer {jwt_token_default}"})
    assert response.status_code == 200


def test_default_lowercase_authorization_header_success(jwt_token_default):
    """
    Test that access to the protected route is granted with a valid JWT token
    in a lowercase Authorization header.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/default", headers={"authorization": f"Bearer {jwt_token_default}"})
    assert response.status_code == 200


def test_default_decoded_success(jwt_token_default):
    """
    Test that access to the protected route is successful and returns decoded token with the correct information.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/default", headers={"Authorization": f"Bearer {jwt_token_default}"})
    assert response.status_code == 200
    assert "decoded_token" in response.json()
    assert response.json().get("decoded_token", {}).get("sub") == "1234567890"


def test_default_denied_bad_token(jwt_token_default):
    """
    Test that access to the protected route is denied with an invalid token.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/default", headers={"Authorization": f"Bearer {jwt_token_default}invalid"})
    assert response.status_code == 403


def test_audience_denied(jwt_token_audience):
    """
    Test that access to the protected route with audience is denied without a token.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/audience", headers={"Authorization": f"Bearer {jwt_token_audience}invalid"})
    assert response.status_code == 403


def test_audience_success(jwt_token_audience):
    """
    Test that access to the protected route with audience is granted with a valid JWT token.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/audience", headers={"Authorization": f"Bearer {jwt_token_audience}"})
    assert response.status_code == 200


def test_audience_mismatch_fail(jwt_token_audience):
    """
    Test that access to the protected route with mismatched audience is denied.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/audience_mismatch_fail", headers={"Authorization": f"Bearer {jwt_token_audience}"})
    assert response.status_code == 403


def test_audience_mismatch_pass(jwt_token_audience):
    """
    Test that access to the protected route with mismatched audience is allowed when verification is disabled.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/audience_mismatch_pass", headers={"Authorization": f"Bearer {jwt_token_audience}"})
    assert response.status_code == 200


def test_issuer_denied(jwt_token_issuer):
    """
    Test that access to the protected route with issuer is denied without a token.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/issuer", headers={"Authorization": f"Bearer {jwt_token_issuer}invalid"})
    assert response.status_code == 403


def test_issuer_success(jwt_token_issuer):
    """
    Test that access to the protected route with issuer is granted with a valid JWT token.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/issuer", headers={"Authorization": f"Bearer {jwt_token_issuer}"})
    assert response.status_code == 200


def test_issuer_mismatch_fail(jwt_token_issuer):
    """
    Test that access to the protected route with mismatched issuer is denied.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/issuer_mismatch_fail", headers={"Authorization": f"Bearer {jwt_token_issuer}"})
    assert response.status_code == 403


def test_issuer_mismatch_pass(jwt_token_issuer):
    """
    Test that access to the protected route with mismatched issuer is allowed when verification is disabled.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/issuer_mismatch_pass", headers={"Authorization": f"Bearer {jwt_token_issuer}"})
    assert response.status_code == 200


def test_iat_future_denied(jwt_token_iat_future):
    """
    Test that access to the protected route is denied with a JWT token that has an iat in the future.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/default", headers={"Authorization": f"Bearer {jwt_token_iat_future}"})
    assert response.status_code == 403


def test_iat_future_pass(jwt_token_iat_future):
    """
    Test that access to the protected route is granted with a JWT token that has an iat in the future
    when iat verification is disabled.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/iat_future_pass", headers={"Authorization": f"Bearer {jwt_token_iat_future}"})
    assert response.status_code == 200


def test_leeway(jwt_token_iat_future_short_leeway):
    """
    Test that access to the protected route is granted with a JWT token that has an iat in the near future
    when leeway is provided.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/leeway", headers={"Authorization": f"Bearer {jwt_token_iat_future_short_leeway}"})
    assert response.status_code == 200


def test_leeway_fail(jwt_token_iat_future_short_leeway):
    """
    Test that access to the protected route is denied with a JWT token that has an iat in the near future
    when leeway is insufficient.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/leeway_fail", headers={"Authorization": f"Bearer {jwt_token_iat_future_short_leeway}"})
    assert response.status_code == 403


def test_default_state_success(jwt_token_default):
    """
    Test that access to the protected route is granted and decoded token is stored in request state.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/default_state", headers={"Authorization": f"Bearer {jwt_token_default}"})
    assert response.status_code == 200
    assert "decoded_token" in response.json()
    assert response.json().get("decoded_token", {}).get("sub") == "1234567890"


def test_jwks_protected_success(jwt_token_default):
    """
    Test that access to the protected route is granted with a valid JWT token when JWKS endpoint requires authentication.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/jwks_protected", headers={"Authorization": f"Bearer {jwt_token_default}"})
    assert response.status_code == 200


def test_jwks_protected_fail(jwt_token_default):
    """
    Test that access to the protected route is denied when JWKS endpoint authentication fails when JWKS endpoint requires authentication.
    """
    response = requests.get(f"{API_SERVER_URL}/protected/jwks_protected_fail", headers={"Authorization": f"Bearer {jwt_token_default}"})
    assert response.status_code == 403
