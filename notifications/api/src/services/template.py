from uuid import UUID

from db.postgres import get_db_session
from fastapi import Depends
from models.notifications import Content
from services.db_service import RelationalDB
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


class ContentService:
    def __init__(self, db_session):
        self.db = db_session

    async def get(self, content_id):
        query = select(Content).where(Content.content_id == content_id)
        result = await self.db.exec(query)
        db_obj = result.one_or_none()
        if not db_obj:
            return None
        return db_obj.content

    async def add(self, templ: Content):
        self.db.add(templ)
        await self.db.commit()
        await self.db.refresh(templ)
        return True

    async def delete(self, content_id: UUID):
        query = select(Content).where(Content.content_id == content_id)
        result = await self.db.exec(query)
        db_obj = result.one_or_none()
        if not db_obj:
            return None
        await self.db.delete(db_obj)
        await self.db.commit()
        return True


def get_template_service(
    db_session: AsyncSession = Depends(get_db_session),
) -> RelationalDB:
    return ContentService(db_session)
