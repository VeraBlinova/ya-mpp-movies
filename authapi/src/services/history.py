import enum
from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from user_agents import parse

from db.postgres import get_db_session
from models.history import HistoryBase, History
from models.user import User
from services.db_service import RelationalDB, UserGroupDB


class HistoryService:
    def __init__(self, login, db_session):
        self.db = db_session
        self.login = login
        self.user_obj = UserGroupDB(db_session, User)

    async def _get_device_type(self, user_agent: str):
        parsed_ua = parse(user_agent)
        if parsed_ua.is_mobile:
            return 'mobile'
        elif parsed_ua.is_tablet:
            return 'tablet'
        return 'web'

    async def get(self, limit: int = 10, offset: int = 0):
        id = await self.user_obj.get_by_login(self.login)
        query = (
            select(History)
            .where(History.user_id == id)
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.exec(query)
        return result.fetchall()

    async def update(self, user_agent):
        id = await self.user_obj.get_by_login(self.login)
        device_type = await self._get_device_type(user_agent)
        hist_rec = History(
            user_id=id, user_agent=user_agent, user_device_type=device_type
        )
        self.db.add(hist_rec)
        await self.db.commit()
        await self.db.refresh(hist_rec)
        return True


def get_history_service(
    login, db_session: AsyncSession = Depends(get_db_session)
) -> RelationalDB:
    return HistoryService(login, db_session)
