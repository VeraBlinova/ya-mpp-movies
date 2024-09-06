from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi_limiter.depends import RateLimiter

from services.history import get_history_service
from services.jwt import JWTService, get_jwt_service
from services.users import UserService, get_user_service

router = APIRouter()

from typing import Annotated

from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import settings
from db.postgres import get_db_session
from db.redis_db import get_redis
from decorators import jwt_refresh_required, jwt_required
from models.user import UserLogin


@AuthJWT.token_in_denylist_loader
async def check_if_token_in_denylist(
    decrypted_token,
):
    redis = await get_redis()
    jti = decrypted_token['jti']
    entry = await redis.get(jti)
    return (entry is not None) and (entry == 'true')


@AuthJWT.load_config
def get_config():
    return settings.jwt


@router.post(
    '/login',
    summary='User Login',
    description='Authenticate a user and return JWT tokens.',
)
async def login(
    user: UserLogin,
    jwt_service: JWTService = Depends(get_jwt_service),
    db_session: AsyncSession = Depends(get_db_session),
    user_service: UserService = Depends(get_user_service),
    user_agent: Annotated[str | None, Header()] = None,
):
    """Login endpoint, returns pair of access and refresh tokens."""
    user_id = await user_service.get_by_login(user.login)
    user_db = await user_service.get_by_id(user_id)
    if user_db is None or not user_db.check_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Bad login or password',
        )
    tokens = await jwt_service.create_tokens(user.login, user_db.role.name)
    current_history = get_history_service(user.login, db_session)
    await current_history.update(user_agent)
    return tokens


@router.post(
    '/refresh',
    summary='Refresh Access Token',
    description='Refresh an existing access token using a refresh token.',
)
@jwt_refresh_required
async def refresh(
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """Endpoint for refreshing access token. Requires refresh token."""
    """Token in denylist will not be able to access this endpoint"""

    current_user = await jwt_service.get_user()
    new_access_token = await jwt_service.create_access_token(current_user)
    return {'access_token': new_access_token}


@router.post(
    '/access-revoke',
    summary='Revoke Access Token',
    description='Revoke an existing access token.',
)
@jwt_required
async def access_revoke(
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """Endpoint for revoking access token. Requires access token."""
    """Token in denylist will not be able to access this endpoint"""

    token = await jwt_service.authorize.get_raw_jwt()
    await jwt_service.revoke_access_token(token)
    return {'detail': 'Access token has been revoked'}


@router.post(
    '/refresh-revoke',
    summary='Revoke Refresh Token',
    description='Revoke an existing refresh token.',
)
@jwt_refresh_required
async def refresh_revoke(
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """Endpoint for revoking refresh token. Requires refresh token."""
    """Token in denylist will not be able to access this endpoint"""

    token = await jwt_service.authorize.get_raw_jwt()
    await jwt_service.revoke_refresh_token(token)
    return {'detail': 'Refresh token has been revoked'}


@router.post(
    '/logout',
    summary='User Logout',
    description='Log out a user by revoking their tokens.',
)
@jwt_required
async def logout(
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """Endpoint for logging out. Requires access token."""
    """Revokes access and refresh tokens."""
    """Token in denylist will not be able to access this endpoint"""

    token = await jwt_service.authorize.get_raw_jwt()
    await jwt_service.revoke_tokens(token)
    return {'detail': 'User logged out'}


# A token in denylist will not be able to access this any more
@router.get(
    '/protected',
    summary='Protected Endpoint',
    description='Access a protected resource using an access token.',
)
@jwt_required
async def protected(
    jwt_service: JWTService = Depends(get_jwt_service),
):

    current_user = await jwt_service.get_user()
    return {'user': current_user}
