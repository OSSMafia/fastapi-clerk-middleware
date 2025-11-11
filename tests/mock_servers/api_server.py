from fastapi import Depends, FastAPI, Request
import uvicorn

from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer

app = FastAPI()

SERVER_URL = "http://mock_jwks_server:8000/.well-known/jwks.json"
SERVER_URL_PROTECTED = "http://mock_jwks_server:8000/protected/.well-known/jwks.json"

auth_default = ClerkHTTPBearer(
    config=ClerkConfig(
        jwks_url=SERVER_URL,
    ),
)
auth_default_state = ClerkHTTPBearer(
    config=ClerkConfig(
        jwks_url=SERVER_URL,
    ),
    add_state=True,
)
auth_audience = ClerkHTTPBearer(
    config=ClerkConfig(
        jwks_url=SERVER_URL,
        audience="test",
        verify_aud=True,
    ),
)
auth_audience_mismatch_fail = ClerkHTTPBearer(
    config=ClerkConfig(
        jwks_url=SERVER_URL,
        audience="test_mismatch",
        verify_aud=True,
    ),
)
auth_audience_mismatch_pass = ClerkHTTPBearer(
    config=ClerkConfig(
        jwks_url=SERVER_URL,
        audience="test_mismatch",
        verify_aud=False,
    ),
)
auth_issuer = ClerkHTTPBearer(
    config=ClerkConfig(
        jwks_url=SERVER_URL,
        issuer="test_issuer",
        verify_iss=True,
    ),
)
auth_issuer_mismatch_fail = ClerkHTTPBearer(
    config=ClerkConfig(
        jwks_url=SERVER_URL,
        issuer="test_issuer_mismatch",
        verify_iss=True,
    ),
)
auth_issuer_mismatch_pass = ClerkHTTPBearer(
    config=ClerkConfig(
        jwks_url=SERVER_URL,
        issuer="test_issuer_mismatch",
        verify_iss=False,
    ),
)
auth_iat_future_pass = ClerkHTTPBearer(
    config=ClerkConfig(
        jwks_url=SERVER_URL,
        verify_iat=False,
    ),
)
auth_leeway = ClerkHTTPBearer(
    config=ClerkConfig(
        jwks_url=SERVER_URL,
        leeway=20,
    ),
)
auth_leeway_fail = ClerkHTTPBearer(
    config=ClerkConfig(
        jwks_url=SERVER_URL,
        leeway=5,
    ),
)
auth_jwks_protected = ClerkHTTPBearer(
    config=ClerkConfig(
        jwks_url=SERVER_URL_PROTECTED,
        jwks_headers={"X-API-KEY": "test_api_key"},
    ),
)
auth_jwks_protected_fail = ClerkHTTPBearer(
    config=ClerkConfig(
        jwks_url=SERVER_URL_PROTECTED,
    ),
)


@app.get("/protected/default")
async def protected_route_default(credentials=Depends(auth_default)):
    return {"status": "OK", "decoded_token": credentials.decoded}


@app.get("/protected/audience")
async def protected_route_audience(credentials=Depends(auth_audience)):
    return {"status": "OK", "decoded_token": credentials.decoded}


@app.get("/protected/audience_mismatch_fail")
async def protected_route_audience_mismatch_fail(credentials=Depends(auth_audience_mismatch_fail)):
    return {"status": "OK", "decoded_token": credentials.decoded}


@app.get("/protected/audience_mismatch_pass")
async def protected_route_audience_mismatch_pass(credentials=Depends(auth_audience_mismatch_pass)):
    return {"status": "OK", "decoded_token": credentials.decoded}


@app.get("/protected/issuer")
async def protected_route_issuer(credentials=Depends(auth_issuer)):
    return {"status": "OK", "decoded_token": credentials.decoded}


@app.get("/protected/issuer_mismatch_fail")
async def protected_route_issuer_mismatch_fail(credentials=Depends(auth_issuer_mismatch_fail)):
    return {"status": "OK", "decoded_token": credentials.decoded}


@app.get("/protected/issuer_mismatch_pass")
async def protected_route_issuer_mismatch_pass(credentials=Depends(auth_issuer_mismatch_pass)):
    return {"status": "OK", "decoded_token": credentials.decoded}


@app.get("/protected/iat_future_pass")
async def protected_route_iat_future_pass(credentials=Depends(auth_iat_future_pass)):
    return {"status": "OK", "decoded_token": credentials.decoded}


@app.get("/protected/leeway")
async def protected_route_leeway(credentials=Depends(auth_leeway)):
    return {"status": "OK", "decoded_token": credentials.decoded}


@app.get("/protected/leeway_fail")
async def protected_route_leeway_fail(credentials=Depends(auth_leeway_fail)):
    return {"status": "OK", "decoded_token": credentials.decoded}


@app.get("/protected/default_state", dependencies=[Depends(auth_default_state)])
async def protected_route_default_state(request: Request):
    return {"status": "OK", "decoded_token": request.state.clerk_auth.decoded}


@app.get("/protected/jwks_protected")
async def protected_route_jwks_protected(credentials=Depends(auth_jwks_protected)):
    return {"status": "OK", "decoded_token": credentials.decoded}


@app.get("/protected/jwks_protected_fail")
async def protected_route_jwks_protected_fail(credentials=Depends(auth_jwks_protected_fail)):
    return {"status": "OK", "decoded_token": credentials.decoded}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
