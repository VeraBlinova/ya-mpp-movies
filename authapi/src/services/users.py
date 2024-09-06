from datetime import datetime
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlmodel.ext.asyncio.session import AsyncSession
from werkzeug.security import generate_password_hash

from db.postgres import get_db_session
from models.user import User, UserCreate, UserRead, UserUpdate
from services.db_service import get_db_service


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_db = get_db_service(User, session)

    async def get_by_login(self, login: str) -> UUID | None:
        user = await self.user_db.get_by_login(login)
        if user is None:
            return None
        return user

    async def get_by_id(self, user_id: UUID) -> UserRead | None:
        try:
            if not isinstance(user_id, UUID):
                user_id = UUID(user_id)
        except ValueError:
            raise HTTPException(status_code=400, detail='Invalid UUID format')

        try:
            user = await self.user_db.get(user_id)
            if user is None:
                return None
            return user
        except NoResultFound:
            raise HTTPException(status_code=404, detail='User not found')

    async def create(self, user: UserCreate) -> UserCreate:
        db_user = User(**user.model_dump())
        db_user.password = generate_password_hash(user.password)
        result = await self.user_db.create(db_user)
        return result

    async def update(self, user_id: UUID, user_data: UserUpdate) -> UserRead:
        user = await self.user_db.get(user_id)
        for key, value in user_data.dict(exclude_unset=True).items():
            if value:
                setattr(user, key, value)
        return await self.user_db.update(user)


def get_user_service(db: AsyncSession = Depends(get_db_session)):
    return UserService(db)
