from uuid import UUID

from bson import Binary
from pydantic import BaseModel, Field


# Модель данных для лайков
class Like(BaseModel):
    rate: int = Field(ge=0, le=10)



class LikeCreate(Like):
    id: UUID = Field(default_factory=UUID)
    user_id: UUID = Field(default_factory=UUID)
    liked_id: UUID = Field(default_factory=UUID)

    def mongo_dict(self):
        return {
            'id': Binary.from_uuid(self.id),
            'user_id': Binary.from_uuid(self.user_id),
            'liked_id': Binary.from_uuid(self.liked_id),
            'rate': self.rate
        }


class LikeRead(LikeCreate):
    pass


class LikeUpdate(Like):
    pass
