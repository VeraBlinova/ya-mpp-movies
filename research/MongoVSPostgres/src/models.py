from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from bson import Binary

class MongoUUID:
    def __init__(self, id: UUID):
        self.id = Binary.from_uuid(id)


class BaseData(BaseModel):
    id: UUID
    datetime: datetime

    def to_mongo(self):
        return {
            "id": MongoUUID(self.id).id,
            "datetime": self.datetime
        }

class Bookmark(BaseData):
    user_id: UUID
    movie_id: UUID

    def to_mongo(self):
        res = super().to_mongo()
        res["user_id"] = MongoUUID(self.user_id).id
        res["movie_id"] = MongoUUID(self.movie_id).id
        return res

class Like(BaseData):
    user_id: UUID
    liked_id: UUID
    rate: int

    def to_mongo(self):
        res = super().to_mongo()
        res["user_id"] = MongoUUID(self.user_id).id
        res["liked_id"] = MongoUUID(self.liked_id).id
        res["rate"] = self.rate
        return res


class Review(BaseData):
    user_id: UUID
    movie_id: UUID
    text: str

    def to_mongo(self):
        res = super().to_mongo()
        res["user_id"] = MongoUUID(self.user_id).id
        res["movie_id"] = MongoUUID(self.movie_id).id
        res["text"] = self.text
        return res
