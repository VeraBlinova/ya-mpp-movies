from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID

from pydantic import BaseModel


class TypeMessage(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class BaseEvent(BaseModel):
    notification_type: TypeMessage
    created: datetime


class RegistrationEvent(BaseEvent):
    user_id: UUID
    subject: str = "Registration"


class NewMovieEvent(BaseEvent):
    movie_id: UUID
    subject: str = "New movie"


class CustomEvent(BaseEvent):
    user_id: UUID
    template_id: UUID
    subject: str
    text: str
    event_type: str
