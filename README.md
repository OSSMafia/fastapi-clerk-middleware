# FastAPI Clerk Auth Middleware


FastAPI Auth Middleware for [Clerk](https://clerk.com)

Easily setup authentication on your API routes using your Clerk JWKS endpoint.

## Install
```bash
pip install fastapi-clerk-auth
```

## Basic Usage
```python
from fastapi import FastAPI, Depends
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

clerk_config = ClerkConfig(jwks_url="https://example.com/.well-known/jwks.json") # Use your Clerk JWKS endpoint

clerk_auth_guard = ClerkHTTPBearer(config=clerk_config)

@app.get("/")
async def read_root(credentials: HTTPAuthorizationCredentials | None = Depends(clerk_auth_guard)):
    return JSONResponse(content=jsonable_encoder(credentials))
```

The returned `credentials` model will either be of type `None` or `HTTPAuthorizationCredentials`. If the model is populated it will have the following properties:
- scheme
    - Indicates the scheme of the Authorization header (Bearer) 
- credentials
    - Raw token received from the Authorization header
- decoded
    - The payload of the decoded token

## Auto Errors
By default the middleware automatically returns 403 errors if the token is missing or invalid. You can disable that behavior by setting the following:
```python
clerk_config = ClerkConfig(jwks_url="https://example.com/.well-known/jwks.json", auto_error=False)
```
This will allow requests to reach the endpoint for additional logic or error handling.
