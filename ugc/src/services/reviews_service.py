from uuid import UUID, uuid4
from datetime import datetime

import requests

from db import get_database
from core.config import settings
from models.likes import LikeRead
from models.models import MongoUUID
from models.reviews import ReviewCreate, ReviewRead, ReviewUpdate
class ReviewService:
    def __init__(self):
        self.db = get_database()

    async def create_review(self, jwt, movie_id, text) -> ReviewRead | None:
        headers = {
            'Authorization': jwt,
            'X-Request-Id': str(uuid4()),
        }
        response = requests.get(settings.auth.AUTHAPI, headers=headers)
        user = response.json()['login']
        user_id = response.json()['id']
        review = ReviewCreate(id=uuid4(),
                              author_id=user_id,
                              author=user,
                              movie_id=movie_id,
                              text=text,
                              pub_date=datetime.now())
        doc = await self.db.reviews.insert_one(review.mongo_dict())
        if doc.acknowledged:
            return ReviewRead(_id=doc.inserted_id, **review.dict())

        return None

    async def get_review(self, review_id) -> ReviewRead | None:
        doc = await self.db.reviews.find_one({'id': MongoUUID(review_id).uuid})
        if not doc:
            return None
        doc['likes'] = [LikeRead(**like).dict() for like in doc['likes']]
        return ReviewRead(**doc)

    async def delete_review(self, review_id) -> UUID | None:
        doc = await self.db.reviews.delete_one({'id': MongoUUID(review_id).uuid})
        if doc.deleted_count > 0:
            return UUID(review_id)
        return None

    async def update_review(self, review_id, text) -> ReviewRead | None:
        review = await self.get_review(review_id)
        review_upd = ReviewUpdate(text=text, pub_date=datetime.now())
        doc = await self.db.reviews.update_one(review.mongo_dict(), {'$set': review_upd.mongo_dict()},
                                            upsert=True)
        if doc.modified_count > 0:
            review = await self.get_review(review_id)
            return review
        return None

    async def get_user_reviews(self, jwt) -> list[ReviewRead] | None:
        headers = {
            'Authorization': jwt,
            'X-Request-Id': str(uuid4()),
        }
        response = requests.get(settings.auth.AUTHAPI, headers=headers)
        user_id = response.json()['id']
        docs = [ReviewRead(**doc) for doc in await self.db.reviews.find({'author_id': MongoUUID(user_id).uuid})]
        if not docs:
            return None
        return docs
        # Дополнительные действия после обновления


def get_review_service():
    return ReviewService()
