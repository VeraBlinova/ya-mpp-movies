from uuid import UUID, uuid4

import requests

from db import get_database
from core.config import settings
from models.bookmarks import Bookmark, BookmarkRead
from models.models import MongoUUID

class BookmarkService:
    def __init__(self):
        self.db = get_database()

    async def create_bookmark(self, jwt, movie_id) -> BookmarkRead | None:
        headers = {
            'Authorization': jwt,
            'X-Request-Id': str(uuid4()),
        }
        response = requests.get(settings.auth.AUTHAPI, headers=headers)
        user_id = response.json()['id']
        bookmark = Bookmark(id=uuid4(), user_id=user_id, movie_id=movie_id)
        doc = await self.db.bookmarks.insert_one(bookmark.mongo_dict())
        if doc.acknowledged:
            return BookmarkRead(_id=doc.inserted_id, **bookmark.dict())

        return None

    async def get_bookmark(self, bookmark_id) -> BookmarkRead | None:
        doc = await self.db.bookmarks.find_one({'id': MongoUUID(bookmark_id).uuid})
        if not doc:
            return None
        return BookmarkRead(**doc)

    async def delete_bookmark(self, bookmark_id) -> UUID | None:
        deleted = await self.db.bookmarks.delete_one({'id': MongoUUID(bookmark_id).uuid})
        if deleted.deleted_count > 0:
            return UUID(bookmark_id)
        return None

    async def get_user_bookmarks(self, jwt) -> list[BookmarkRead] | None:
        headers = {
            'Authorization': jwt,
            'X-Request-Id': str(uuid4()),
        }
        response = requests.get(settings.auth.AUTHAPI, headers=headers)
        user_id = response.json()['id']
        docs = self.db.bookmarks.find({'user_id': MongoUUID(user_id).uuid})
        if not docs:
            return None
        return [BookmarkRead(**doc) for doc in docs]


def get_bookmark_service():
    return BookmarkService()