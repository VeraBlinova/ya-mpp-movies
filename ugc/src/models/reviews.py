# Модель данных для комментариев
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from bson import Binary
from pydantic.v1 import BaseModel

from models.likes import LikeRead


class Review(BaseModel):
    text: str
    pub_date: datetime

    def mongo_dict(self):
        return {
            'text': self.text,
            'pub_date': self.pub_date,
        }


class ReviewCreate(Review):
    id: UUID
    author_id: UUID
    movie_id: UUID
    author: str

    def mongo_dict(self):
        return {
            'id': Binary.from_uuid(self.id),
            'author_id': Binary.from_uuid(self.author_id),
            'movie_id': Binary.from_uuid(self.movie_id),
            'text': self.text,
            'pub_date': self.pub_date,
            'author': self.author
        }


class ReviewRead(ReviewCreate):
    likes: list = []

    class Config:
        arbitrary_types_allowed = True


class ReviewUpdate(Review):
    pass
