import requests


def test_jwks_endpoint():
    response = requests.get("http://mock_jwks_server:8000/.well-known/jwks.json")
    assert response.status_code == 200
    jwks = response.json()
    assert "keys" in jwks


def test_protected_route_access_granted(jwt_token):
    response = requests.get("http://mock_api_server:8001/protected", headers={"Authorization": f"Bearer {jwt_token}"})
    assert response.status_code == 200


def test_protected_route_access_granted_decoded(jwt_token):
    response = requests.get("http://mock_api_server:8001/protected", headers={"Authorization": f"Bearer {jwt_token}"})
    assert response.status_code == 200
    assert "decoded_token" in response.json()
    assert response.json().get("decoded_token", {}).get("sub") == "1234567890"


def test_protected_route_access_denied():
    response = requests.get("http://mock_api_server:8001/protected")
    assert response.status_code == 403


def test_protected_route_access_denied_bad_token(jwt_token):
    response = requests.get("http://mock_api_server:8001/protected", headers={"Authorization": f"Bearer {jwt_token}invalid"})
    assert response.status_code == 403
