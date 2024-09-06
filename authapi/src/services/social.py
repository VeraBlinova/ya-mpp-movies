from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from db.postgres import get_db_session
from models.social import social_account
from services.db_service import RelationalDB


class SocialService:
    def __init__(self, db_session):
        self.db = db_session

    async def get(self,social_name,social_id):
        query = (
            select(social_account)
            .where(social_account.social_id == social_id,social_account.social_name == social_name)
        )
        result = await self.db.exec(query)
        return result.fetchall()
    
    async def add(self, user_id, social_name,social_id):
        soc_rec = social_account(
            user_id=user_id, social_id=social_id, social_name=social_name
        )
        self.db.add(soc_rec)
        await self.db.commit()
        await self.db.refresh(soc_rec)
        return True


def get_social_service(
    db_session: AsyncSession = Depends(get_db_session)
) -> RelationalDB:
    return SocialService(db_session)
