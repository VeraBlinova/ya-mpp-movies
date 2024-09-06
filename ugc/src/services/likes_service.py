import uuid
from datetime import datetime

import requests

from db import get_database
from core.config import settings
from models.likes import LikeCreate, LikeRead, LikeUpdate
from models.models import MongoUUID


class LikesService:
    def __init__(self):
        self.db = get_database()

    async def create_like(self, jwt, liked_id) -> LikeRead | None:
        headers = {
            'Authorization': jwt,
            'X-Request-Id': str(uuid.uuid4()),
        }
        response = requests.get(settings.auth.AUTHAPI, headers=headers)
        user_id = response.json()['id']
        like = LikeCreate(id=uuid.uuid4(), user_id=user_id, liked_id=liked_id, rate=10)
        doc = await self.db.likes.insert_one(like.mongo_dict())
        if doc.acknowledged:
            inserted_like = await self.get_like(like.id)
            updated = await self.db.reviews.update_one({'id': MongoUUID(liked_id).uuid},
                                                    {'$push': {'likes': inserted_like.mongo_dict()}})
            if updated.modified_count > 0:
                return LikeRead(**like.dict())

        return None

    async def get_like(self, like_id) -> LikeRead | None:
        doc = await self.db.likes.find_one({'id': MongoUUID(like_id).uuid})
        if not doc:
            return None
        return LikeRead(**doc)

    async def delete_like(self, like_id) -> LikeRead | None:
        doc = await self.db.likes.delete_one({'id': MongoUUID(like_id).uuid})
        if doc.deleted_count > 0:
            return LikeRead(**doc)
        return None

    async def update_rate(self, like_id, rate) -> LikeRead | None:
        like = await self.get_like(like_id)
        LikeUpdate(rate=rate)
        doc = await self.db.likes.update_one(like.dict())
        if doc.modified_count > 0:
            return await self.get_like(like_id)
        return None


def get_likes_service():
    return LikesService()
