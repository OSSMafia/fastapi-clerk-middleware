import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()


@app.get("/.well-known/jwks.json")
async def jwks():
    with open("./mock_files/test_jwks.json") as jwks_file:
        jwks_data = json.load(jwks_file)
    return JSONResponse(content=jwks_data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
