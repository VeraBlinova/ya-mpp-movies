import uuid
from datetime import datetime
from typing import Optional, List

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel
from werkzeug.security import check_password_hash

from models.role import Role


class UserBase(SQLModel):
    """
    Base User model. Serves as pydantic model for data validation.
    """

    login: str = Field(unique=True, max_length=255, index=True)
    password: str = Field(max_length=255)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=datetime.utcnow,
    )

    role_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key='roles.id'
    )

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f'<User {self.login}>'


class User(UserBase, table=True):
    """
    Model of the Users db table.
    `id` is optional because it's autocreated by database.
    """

    __tablename__ = 'users'


    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True
    )
    role: Optional[Role] = Relationship(back_populates='users',sa_relationship_kwargs={'lazy': 'selectin'})
    historys: List['History'] = Relationship(back_populates='user',sa_relationship_kwargs={"cascade": "all,delete",'lazy': 'selectin'})
    socials: List['social_account'] = Relationship(back_populates='user',sa_relationship_kwargs={"cascade": "all,delete",'lazy': 'selectin'})



class UserCreate(UserBase):
    """Data model for creating a User."""

    pass


class UserRead(UserBase):
    """Data model for User object api response."""

    id: uuid.UUID

    def __init__(self, id: uuid.UUID, **kwargs):
        super().__init__(**kwargs)
        self.id = id



class UserUpdate(SQLModel):
    """
    Data model for updating a user db entry.
    All fields are optional to be able to update any of them.
    """

    login: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None


class UserLogin(SQLModel):
    login: str = Field(unique=True, max_length=255, index=True)
    password: str = Field(max_length=255)
