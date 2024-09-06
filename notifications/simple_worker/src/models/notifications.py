from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class Notification(SQLModel, table=True):
    __tablename__ = "notifications"
    notification_id: Optional[UUID] = Field(primary_key=True, default_factory=uuid4)
    content_id: Optional[UUID] = Field(nullable=False, foreign_key="content.content_id")
    recipient_email: Optional[str] = Field(max_length=100, nullable=False)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True)), default_factory=datetime.utcnow
    )
    type: Optional[str] = Field(max_length=50, nullable=False)
    text: Optional[str] = Field(max_length=10000, nullable=False)
    schedule_id: Optional[UUID] = Field(foreign_key="notification_schedule.schedule_id")

    content: str = Field(nullable=False, foreign_key="content.content")
    schedule: Optional[UUID] = Field(nullable=False, foreign_key="content.content_id")
