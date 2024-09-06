import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKeyConstraint, UniqueConstraint, text
from sqlmodel import Column, DateTime, Field, Relationship, SQLModel

from models.user import User


def create_partition(target, connection, **kw) -> None:
    connection.execute(
        text(
            """CREATE TABLE IF NOT EXISTS "history_web" PARTITION OF "history" FOR VALUES IN ('web')"""
        )
    )
    connection.execute(
        text(
            """CREATE TABLE IF NOT EXISTS "history_mobile" PARTITION OF "history" FOR VALUES IN ('mobile')"""
        )
    )
    connection.execute(
        text(
            """CREATE TABLE IF NOT EXISTS "history_tablet" PARTITION OF "history" FOR VALUES IN ('tablet')"""
        )
    )


class HistoryBase(SQLModel):
    """
    Base data model of login history entry.
    Serves as pydantic model for data validation.
    """

    user_id: uuid.UUID = Field(foreign_key='users.id')
    user_agent: str = Field(max_length=255)
    user_device_type: str = Field(max_length=20, primary_key=True)
    auth_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=datetime.utcnow,
    )


class History(HistoryBase, table=True):
    """
    Model of the `history` db table.
    `id` is optional because it's autocreated by database.
    """

    __tablename__ = 'history'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        UniqueConstraint('id', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_device_type)',
            'listeners': [('after_create', create_partition)],
        },
    )

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True
    )
    user: Optional[User] = Relationship(
        back_populates='historys',
        sa_relationship_kwargs={'cascade': 'all,delete', 'lazy': 'selectin'},
    )

    def __repr__(self) -> str:
        return f'<Signin on {self.auth_at} with {self.user_agent}>'
