import json

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
import uvicorn

app = FastAPI()

api_key_header = APIKeyHeader(name="X-API-KEY")


@app.get("/.well-known/jwks.json")
async def jwks():
    with open("./mock_files/test_jwks.json") as jwks_file:
        jwks_data = json.load(jwks_file)
    return JSONResponse(content=jwks_data)


@app.get("/protected/.well-known/jwks.json")
async def jwks_protected(api_key: str = Depends(api_key_header)):
    if api_key != "test_api_key":
        raise HTTPException(status_code=403, detail="Forbidden")

    with open("./mock_files/test_jwks.json") as jwks_file:
        jwks_data = json.load(jwks_file)
    return JSONResponse(content=jwks_data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
