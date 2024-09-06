from functools import wraps

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException, status

from services.jwt import JWTService, get_jwt_service


def roles_required(roles_list: list[str]):
    def decorator(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            authorize: AuthJWT = kwargs['jwt_service'].authorize
            jwt = await authorize.get_raw_jwt()
            role = jwt.get('role')
            if not role or role not in roles_list:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='This operation is forbidden for you',
                )
            return await function(*args, **kwargs)

        return wrapper

    return decorator


def jwt_required(fn):
    @wraps(fn)
    async def decorator(
        *args, jwt_service: JWTService = Depends(get_jwt_service), **kwargs
    ):
        await jwt_service.authorize.jwt_required()
        return await fn(*args, jwt_service=jwt_service, **kwargs)

    return decorator


def jwt_refresh_required(fn):
    @wraps(fn)
    async def decorator(
        *args, jwt_service: JWTService = Depends(get_jwt_service), **kwargs
    ):
        await jwt_service.authorize.jwt_refresh_token_required()
        return await fn(*args, jwt_service=jwt_service, **kwargs)

    return decorator
