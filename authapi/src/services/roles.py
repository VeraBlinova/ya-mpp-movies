from uuid import UUID

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from db.postgres import get_db_session
from models.role import Role, RoleCreate, RoleRead, RoleUpdate
from services.db_service import RelationalDB, get_db_service


class RolesService:
    def __init__(self, repository: RelationalDB) -> None:
        self._repository = repository

    async def get(self, uuid: UUID) -> RoleRead:
        return await self._repository.get(uuid)

    async def get_multi(
        self, limit: int = 50, offset: int = 0
    ) -> list[RoleRead]:
        results = await self._repository.get_multi(limit=limit, offset=offset)
        return results

    async def create(self, role_data: RoleCreate):
        role = Role(**role_data.model_dump())
        return await self._repository.create(role)

    async def update(self, uuid: UUID, role_data: RoleUpdate) -> RoleRead:
        return await self._repository.update(uuid, role_data)

    async def delete(self, uuid: UUID):
        await self._repository.delete(uuid)


async def get_roles_service(
    db_session: AsyncSession = Depends(get_db_session),
):
    db_service = get_db_service(db_session=db_session, model=Role)
    return RolesService(repository=db_service)
