from typing import Any
from typing import Optional

from fastapi import HTTPException
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.security import HTTPAuthorizationCredentials as FastAPIHTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
import jwt
from jwt import PyJWKClient
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN
from typing_extensions import Annotated
from typing_extensions import Doc


class ClerkConfig(BaseModel):
    jwks_url: str
    audience: str | None = None
    issuer: str | None = None
    verify_exp: bool = True
    verify_aud: bool = False
    verify_iss: bool = False
    jwks_cache_keys: bool = False
    jwks_max_cached_keys: int = 16
    jwks_cache_set: bool = True
    jwks_lifespan: int = 300
    jwks_headers: Optional[dict[str, Any]] = None
    jwks_client_timeout: int = 30


class HTTPAuthorizationCredentials(FastAPIHTTPAuthorizationCredentials):
    decoded: dict | None = None


class ClerkHTTPBearer(HTTPBearer):
    def __init__(
        self,
        config: ClerkConfig,
        bearerFormat: Annotated[Optional[str], Doc("Bearer token format.")] = None,
        scheme_name: Annotated[
            Optional[str],
            Doc(
                """
                    Security scheme name.

                    It will be included in the generated OpenAPI (e.g. visible at `/docs`).
                    """
            ),
        ] = None,
        description: Annotated[
            Optional[str],
            Doc(
                """
                    Security scheme description.

                    It will be included in the generated OpenAPI (e.g. visible at `/docs`).
                    """
            ),
        ] = None,
        auto_error: Annotated[
            bool,
            Doc(
                """
                    By default, if the HTTP Bearer token not provided (in an
                    `Authorization` header), `HTTPBearer` will automatically cancel the
                    request and send the client an error.

                    If `auto_error` is set to `False`, when the HTTP Bearer token
                    is not available, instead of erroring out, the dependency result will
                    be `None`.

                    This is useful when you want to have optional authentication.

                    It is also useful when you want to have authentication that can be
                    provided in one of multiple optional ways (for example, in an HTTP
                    Bearer token or in a cookie).
                    """
            ),
        ] = True,
        add_state: Annotated[
            bool,
            Doc(
                """
                    By default, the decoded authentication data is returned from the `Depends`
                    on the route function. If you'd like to have the decoded authentication data
                    available in the request state, set this to `True`. This is useful when you
                    want to have the decoded authentication data available in the request state
                    while applying the middleware to multiple routes via a router dependency.
                """
            ),
        ] = False,
        debug_mode: bool = False,
    ):
        super().__init__(
            bearerFormat=bearerFormat,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )
        self.model = HTTPBearerModel(bearerFormat=bearerFormat, description=description)
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error
        self.add_state = add_state
        self.config = config
        self._check_config()
        self.jwks_url: str = config.jwks_url
        self.audience: str | None = config.audience
        self.issuer: str | None = config.issuer
        self.jwks_client: PyJWKClient = PyJWKClient(
            uri=config.jwks_url,
            cache_keys=config.jwks_cache_keys,
            max_cached_keys=config.jwks_max_cached_keys,
            cache_jwk_set=config.jwks_cache_set,
            lifespan=config.jwks_lifespan,
            headers=config.jwks_headers,
            timeout=config.jwks_client_timeout,
        )
        self.add_state = add_state
        self.debug_mode = debug_mode

    def _check_config(self) -> None:
        if not self.config.audience and self.config.verify_aud:
            raise ValueError("Audience must be set in config because verify_aud is True")
        if not self.config.issuer and self.config.verify_iss:
            raise ValueError("Issuer must be set in config because verify_iss is True")

    def _decode_token(self, token: str) -> dict | None:
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            decoded_token = jwt.decode(
                token,
                key=signing_key.key,
                audience=self.audience,
                issuer=self.issuer,
                algorithms=["RS256"],
                options={
                    "verify_exp": self.config.verify_exp,
                    "verify_aud": self.config.verify_aud,
                    "verify_iss": self.config.verify_iss,
                },
            )
            return dict(jsonable_encoder(decoded_token))
        except Exception as e:
            if self.debug_mode:
                raise e
            return None

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        authorization = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not Authenticated")
            return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="Invalid Authentication Credentials",
                )
            return None

        decoded_token: dict | None = self._decode_token(token=credentials)
        if not decoded_token and self.auto_error:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Invalid Authentication Credentials",
            )
        response = HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials, decoded=decoded_token)
        if self.add_state:
            request.state.clerk_auth = response
        return response
