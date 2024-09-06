from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from fastapi import Depends
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from db.postgres import get_db_session


class RelationalDB(ABC):
    """Abstract base class for relational databases."""

    @abstractmethod
    def get(self, *args, **kwargs):
        ...

    @abstractmethod
    def get_multi(self, *args, **kwargs):
        ...

    @abstractmethod
    def create(self, *args, **kwargs):
        ...

    @abstractmethod
    def update(self, *args, **kwargs):
        ...

    @abstractmethod
    def delete(self, *args, **kwargs):
        ...


class UserGroupDB(RelationalDB):

    def __init__(self, db: AsyncSession, model: Any):
        self.db = db
        self.model = model

    async def get(self, id: UUID):
        query = select(self.model).where(self.model.id == id)
        result = await self.db.exec(query)
        return result.first()

    async def get_by_login(self, login: str):
        query = select(self.model).where(self.model.login == login)
        result = await self.db.exec(query)
        first = result.first()
        if first:
            return first.id
        return None

    async def get_multi(self, limit: int = 50, offset: int = 0):
        query = select(self.model).offset(offset).limit(limit)
        result = await self.db.exec(query)
        return result.fetchall()

    async def create(self, model: Any):
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def update(self, id: UUID):
        query = select(self.model).where(self.model.id == id.id)
        result = await self.db.exec(query)
        db_obj = result.one_or_none()
        if not db_obj:
            return None
        print(f'user in db: {db_obj}')
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, id: UUID):
        query = select(self.model).where(self.model.id == id)
        result = await self.db.exec(query)
        db_obj = result.one_or_none()
        if not db_obj:
            return None
        await self.db.delete(db_obj)
        await self.db.commit()
        return db_obj


def get_db_service(
        model: Any,
        db_session: AsyncSession = Depends(get_db_session)
) -> RelationalDB:
    return UserGroupDB(db_session, model)

