from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from services.users import UserService, get_user_service


class AuthRequest(Request):
    custom_user: User


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self,
        request: Request,
        user_service: UserService = Depends(get_user_service),
    ) -> User | None:
        authorize = AuthJWT(req=request)
        await authorize.jwt_optional()
        user_login = await authorize.get_jwt_subject()
        if not user_login:
            return None
        user_id = await user_service.get_by_login(user_login)
        user = await user_service.get_by_id(user_id)
        return user


async def get_current_user_global(
    request: AuthRequest,
    user: AsyncSession = Depends(JWTBearer()),
):
    request.custom_user = user
