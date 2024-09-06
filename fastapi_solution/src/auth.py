import http
import time

from core.config import settings
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt


def decode_token(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(
            token,
            settings.auth.jwt_secret_key,
            algorithms=[settings.auth.jwt_algorithm],
        )
        return decoded_token if decoded_token['exp'] >= time.time() else None
    except Exception:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request
        )
        if credentials:
            if not credentials.scheme == 'Bearer':
                raise HTTPException(
                    status_code=http.HTTPStatus.UNAUTHORIZED,
                    detail='Invalid authentication scheme.',
                )
            decoded_token = self.parse_token(credentials.credentials)
            if not decoded_token:
                raise HTTPException(
                    status_code=http.HTTPStatus.FORBIDDEN,
                    detail='Invalid token or expired token.',
                )
            return decoded_token
        raise HTTPException(
            status_code=http.HTTPStatus.FORBIDDEN,
            detail='Invalid authorization code.',
        )

    @staticmethod
    def parse_token(jwt_token: str) -> dict | None:
        return decode_token(jwt_token)


security_jwt = JWTBearer()
