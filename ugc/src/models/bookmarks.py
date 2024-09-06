# Модель данных для просмотров
from uuid import UUID
from bson import Binary, binary

from pydantic import BaseModel

class Bookmark(BaseModel):
    id: UUID
    user_id: UUID
    movie_id: UUID

    def mongo_dict(self):
        return {
            'id': Binary.from_uuid(self.id),
            'user_id': Binary.from_uuid(self.user_id),
            'movie_id': Binary.from_uuid(self.movie_id)
        }

class BookmarkRead(Bookmark):
    pass