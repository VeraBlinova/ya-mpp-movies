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
    text: Optional[str] = Field(max_length=10000, nullable=False)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True)), default_factory=datetime.utcnow
    )
    type: Optional[str] = Field(max_length=50, nullable=False)

    schedule_id: Optional[UUID] = Field(foreign_key="notification_schedule.schedule_id")

    content: str = Field(nullable=False, foreign_key="content.content")
    schedule: Optional[UUID] = Field(nullable=False, foreign_key="content.content_id")


class Content(SQLModel, table=True):
    __tablename__ = "content"
    content_id: Optional[UUID] = Field(primary_key=True, default_factory=uuid4)
    content: str = Field(nullable=False)


class NotificationSchedule(SQLModel, table=True):
    __tablename__ = "notification_schedule"
    schedule_id: Optional[UUID] = Field(primary_key=True, default_factory=uuid4)
    frequency: str = Field(max_length=50, nullable=False)


class NotificationHistory(SQLModel, table=True):
    __tablename__ = "notification_history"
    history_id: Optional[UUID] = Field(primary_key=True, default_factory=uuid4)
    notification_id: Optional[UUID] = Field(
        foreign_key="notifications.notification_id", nullable=False
    )
    sent_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)), default_factory=datetime.utcnow
    )

    notification: Optional[UUID] = Field(
        nullable=False, foreign_key="notifications.notification_id"
    )
