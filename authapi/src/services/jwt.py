from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends
from redis.asyncio import Redis

from core.config import settings
from db.redis_db import get_redis
from models.jwt import JWTToken


class JWTService:
    def __init__(self, redis: Redis, authorize: AuthJWT):
        self.redis = redis
        self.authorize = authorize

    async def create_access_token(self, username: str, role: str) -> str:
        access_token = await self.authorize.create_access_token(
            subject=username,
            user_claims={"role": role},
            expires_time=settings.jwt.authjwt_access_expires,
        )
        return access_token

    async def create_refresh_token(self, username: str) -> str:
        refresh_token = await self.authorize.create_refresh_token(
            subject=username,
            expires_time=settings.jwt.authjwt_refresh_expires,
        )
        return refresh_token

    async def create_tokens(self, username: str, role: str) -> JWTToken:
        access_token = await self.create_access_token(username, role)
        refresh_token = await self.create_refresh_token(username)
        return {'access_token': access_token, 'refresh_token': refresh_token}

    async def revoke_access_token(self, token: str):
        jti = token['jti']
        await self.redis.setex(
            jti, settings.jwt.authjwt_access_expires, 'true'
        )

    async def revoke_refresh_token(self, token: str):
        jti = token['jti']
        await self.redis.setex(
            jti, settings.jwt.authjwt_refresh_expires, 'true'
        )

    async def revoke_tokens(self, token: str):
        await self.revoke_access_token(token)
        await self.revoke_refresh_token(token)

    async def get_user(self):
        user = await self.authorize.get_jwt_subject()
        return user


def get_jwt_service(
    redis: Redis = Depends(get_redis),
    authorize: AuthJWT = Depends(),
) -> JWTService:
    return JWTService(redis=redis, authorize=authorize)
