from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

from uuid import UUID
from bson import Binary, binary

# Модель данных для объектов
class Event(BaseModel):  # TODO: Add proper event schema
    key: str
    value: str

class MongoUUID:
    def __init__(self, uuid: UUID|str):
        if isinstance(uuid, str):
            uuid = UUID(uuid)
        self.uuid = Binary.from_uuid(uuid)
    @classmethod
    def to_uuid(cls, binary: Binary):
        return binary.as_uuid()





