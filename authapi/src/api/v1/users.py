from fastapi import APIRouter, Depends, HTTPException, status

from decorators import jwt_required
from models.user import UserCreate, UserRead, UserUpdate
from services.jwt import JWTService, get_jwt_service
from services.users import UserService, get_user_service

router = APIRouter()


@router.post(
    '/signup',
    summary='User Signup',
    description='Register a new user and return JWT tokens.',
)
async def signup(
    user_data: UserCreate,
    jwt_service: JWTService = Depends(get_jwt_service),
    user_service: UserService = Depends(get_user_service),
):
    """Login endpoint, returns a pair of access and refresh tokens."""
    user = await user_service.create(user_data)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Bad login or password',
        )
    user_id = await user_service.get_by_login(user.login)
    user_db = await user_service.get_by_id(user_id)
    tokens = await jwt_service.create_tokens(user.login, user_db.role.name)
    return tokens


@router.get(
    '/profile',
    summary='User Profile',
    description='Get the profile of the currently logged-in user.',
)
@jwt_required
async def profile(
    user_service: UserService = Depends(get_user_service),
    jwt_service: JWTService = Depends(get_jwt_service),
) -> UserRead:
    login = await jwt_service.get_user()
    if login is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Bad login or password',
        )
    user_id = await user_service.get_by_login(login)
    user = await user_service.get_by_id(user_id)
    return user


@router.post(
    '/change-user',
    summary='Update User',
    description='Update the login details of the current user.',
)
@jwt_required
async def change_login(
    user_update: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    jwt_service: JWTService = Depends(get_jwt_service),
) -> UserRead:
    jwt_login = await jwt_service.get_user()
    if jwt_login is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized Access',
        )
    user_id = await user_service.get_by_login(jwt_login)
    return await user_service.update(user_id, user_update)
