import uuid
from datetime import datetime
from typing import List, Optional

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel


class RoleBase(SQLModel):
    """
    Base Role model. Serves as pydantic model for data validation.
    https://sqlmodel.tiangolo.com/#sqlalchemy-and-pydantic
    """

    name: str = Field(unique=True, max_length=50)
    description: Optional[str] = Field(max_length=255)
    is_superuser: bool = False
    is_staff: bool = False
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=datetime.utcnow,
    )

    def __repr__(self) -> str:
        return f'<Role {self.name}>'


class Role(RoleBase, table=True):
    """
    Model of the Roles db table.
    `id` is optional because it's autocreated by database.
    """

    __tablename__ = 'roles'


    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, primary_key=True
    )
    users: List['User'] = Relationship(back_populates='role')


class RoleCreate(RoleBase):
    """Data model for creating a Role."""

    pass


class RoleRead(RoleBase):
    """Data model for Role object api response."""

    id: uuid.UUID


class RoleUpdate(SQLModel):
    """
    Data model for updating a role db entry.
    All fields are optional to be able to update any of them.
    """

    name: Optional[str] = None
    description: Optional[str]
    is_superuser: Optional[bool] = None
    is_staff: Optional[bool] = None
    created_at: Optional[datetime] = None
