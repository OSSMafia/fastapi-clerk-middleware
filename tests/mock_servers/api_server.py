from fastapi import Depends, FastAPI
import uvicorn

from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer

app = FastAPI()

config = ClerkConfig(
    jwks_url="http://mock_jwks_server:8000/.well-known/jwks.json",
)

auth = ClerkHTTPBearer(config=config)


@app.get("/protected")
async def protected_route(credentials=Depends(auth)):
    return {"message": "Access granted", "user": credentials.decoded}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
