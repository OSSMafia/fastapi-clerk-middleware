# FastAPI Clerk Auth Middleware


FastAPI Auth Middleware for [Clerk](https://clerk.com)

## Install
```bash
pip install fastapi-clerk
```

## Basic Usage
```python
from fastapi import FastAPI, Depends
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

clerk_config = ClerkConfig(jwks_url="https://example.com/.well-known/jwks.json") # Use your Clerk JWKS endpoint

clear_auth_guard = ClerkHTTPBearer(config=clerk_config)

@app.get("/")
async def read_root(credentials: HTTPAuthorizationCredentials | None = Depends(clear_auth_guard)):
    return JSONResponse(content=jsonable_encoder(credentials))
```