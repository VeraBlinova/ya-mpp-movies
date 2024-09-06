import uuid
from typing import Optional

from sqlalchemy import ForeignKeyConstraint, UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

from models.user import User


class SocialBase(SQLModel):

    user_id: uuid.UUID = Field(foreign_key='users.id')
    social_name: str = Field(max_length=255)
    social_id: str = Field(max_length=255)



class social_account(SocialBase, table=True):

    __tablename__ = 'social_account'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        UniqueConstraint('social_id', 'social_name'),
    )

    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True
    )
    user: Optional[User] = Relationship(
        back_populates='socials',
        sa_relationship_kwargs={'cascade': 'all,delete', 'lazy': 'selectin'},
    )

