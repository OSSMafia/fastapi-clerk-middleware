# FastAPI Clerk Auth Middleware

[![PyPI version](https://img.shields.io/pypi/v/fastapi-clerk-auth.svg)](https://pypi.org/project/fastapi-clerk-auth/)
[![Python Versions](https://img.shields.io/pypi/pyversions/fastapi-clerk-auth.svg)](https://pypi.org/project/fastapi-clerk-auth/)
[![License](https://img.shields.io/github/license/OSSMafia/fastapi-clerk-middleware)](https://github.com/OSSMafia/fastapi-clerk-middleware/blob/main/LICENSE)

A lightweight, easy-to-use authentication middleware for [FastAPI](https://fastapi.tiangolo.com/) that integrates with [Clerk](https://clerk.com) authentication services.

This middleware allows you to secure your FastAPI routes by validating JWT tokens against your Clerk JWKS endpoint, making it simple to implement authentication in your API.

## Features

- 🔒 Secure API routes with Clerk JWT validation
- 🚀 Simple integration with FastAPI's dependency injection system
- ⚙️ Flexible configuration options (auto error responses, request state access)
- 📝 Decoded token payload accessible in your route handlers

## Installation

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

# Use your Clerk JWKS endpoint
clerk_config = ClerkConfig(jwks_url="https://your-clerk-frontend-api.clerk.accounts.dev/.well-known/jwks.json") 

clerk_auth_guard = ClerkHTTPBearer(config=clerk_config)

@app.get("/")
async def read_root(credentials: HTTPAuthorizationCredentials = Depends(clerk_auth_guard)):
    return JSONResponse(content=jsonable_encoder(credentials))
```

The returned `credentials` model will be an `HTTPAuthorizationCredentials` object with these properties:

- `scheme`: Indicates the scheme of the Authorization header (Bearer) 
- `credentials`: Raw token received from the Authorization header
- `decoded`: The payload of the decoded token

## Configuration Options

### Debug Mode

By default, the middleware suppresses exceptions in order to prevent logging sensitive information. You can change this behavior in the `ClerkHTTPBearer`:

```python
clerk_auth_guard = ClerkHTTPBearer(config=clerk_config, debug_mode=True)  # Set debug_mode=True
```


### Fixing Issued At Time (IAT) Errors

In some instances the system clock of an API may be slightly out-of-sync which can cause issues with verifying the `iat` claim.

This can be solved one of two ways:

1: Disable verifying the `iat` claim, there could be security implications by disabling so make sure it is secure for your use case.

```python
clerk_config = ClerkConfig(
    jwks_url="https://your-clerk-frontend-api.clerk.accounts.dev/.well-known/jwks.json",
    verify_iat=False,
) 

clerk_auth_guard = ClerkHTTPBearer(config=clerk_config)
```

2: Adding `leeway` which is a number of seconds to allow tolerance for drift, it can compensate for out-of-sync clocks.

```python
clerk_config = ClerkConfig(
    jwks_url="https://your-clerk-frontend-api.clerk.accounts.dev/.well-known/jwks.json",
    leeway=5.0,
) 

clerk_auth_guard = ClerkHTTPBearer(config=clerk_config)
```

### Disabling Auto Errors

By default, the middleware automatically returns 403 errors if the token is missing or invalid. You can disable this behavior:

```python
clerk_config = ClerkConfig(
    jwks_url="https://your-clerk-frontend-api.clerk.accounts.dev/.well-known/jwks.json"
) 

clerk_auth_guard = ClerkHTTPBearer(config=clerk_config, auto_error=False)  # Set auto_error=False
```

This allows requests to reach the endpoint for additional logic or custom error handling:

```python
@app.get("/protected")
async def protected_endpoint(credentials: HTTPAuthorizationCredentials | None = Depends(clerk_auth_guard)):
    if not credentials:
        return {"message": "You're not authenticated, but you can still see this limited data"}
    
    # Full access for authenticated users
    return {"message": "Full access granted", "user_data": credentials.decoded}
```

### Adding Auth Data to Request State

You can have the `HTTPAuthorizationCredentials` added to the request state for easier access:

```python
from fastapi import Depends, Request, APIRouter
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

clerk_config = ClerkConfig(
    jwks_url="https://your-clerk-frontend-api.clerk.accounts.dev/.well-known/jwks.json"
) 

clerk_auth_guard = ClerkHTTPBearer(config=clerk_config, add_state=True)

router = APIRouter(prefix="/todo", dependencies=[Depends(clerk_auth_guard)])

@router.get("/")
async def read_todo_list(request: Request):
    auth_data: HTTPAuthorizationCredentials = request.state.clerk_auth
    user_id = auth_data.decoded.get("sub")
    
    # Use user_id to fetch the user's todo items
    return {"message": f"Todo items for user {user_id}"}
```

The class stored in `request.state.clerk_auth` looks like this:
```python
HTTPAuthorizationCredentials(
    decoded: Optional[dict],  # Decoded JWT Token
    scheme: str = "Bearer",
    credentials: str,  # Raw JWT Token
)
```

## Advanced Usage

### Role-Based Access Control

You can implement role-based access control by checking the JWT claims:

```python
from fastapi import Depends, HTTPException, status

def admin_required(credentials: HTTPAuthorizationCredentials = Depends(clerk_auth_guard)):
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    user_roles = credentials.decoded.get("roles", [])
    if "admin" not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required"
        )
    
    return credentials

@app.get("/admin", dependencies=[Depends(admin_required)])
async def admin_only():
    return {"message": "Welcome, admin!"}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
