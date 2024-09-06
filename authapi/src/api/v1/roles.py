import uuid
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from services.jwt import JWTService, get_jwt_service

from auth import AuthRequest
from decorators import roles_required
from models.role import RoleCreate, RoleRead, RoleUpdate
from services.roles import RolesService, get_roles_service

router = APIRouter()


@router.get(
    '/',
    summary='Roles list',
    description='Get the list of existing user roles',
    response_model=list[RoleRead],
)
@roles_required(roles_list=['admin'])
async def get_roles(
    *,
    request: AuthRequest,
    roles_service: RolesService = Depends(get_roles_service),
    jwt_service: JWTService = Depends(get_jwt_service),
) -> list[RoleRead]:
    return await roles_service.get_multi()


@router.get(
    '/{uuid}',
    summary='Roles details',
    description='Get details of the role by its uuid',
    response_model=RoleRead,
)
@roles_required(roles_list=['admin'])
async def get_role(
    request: AuthRequest,
    uuid: UUID,
    roles_service: RolesService = Depends(get_roles_service),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    return await roles_service.get(uuid)


@router.post(
    '/',
    summary='Create role',
    description='Create a new role',
    response_model=RoleRead,
)
@roles_required(roles_list=['admin'])
async def create_role(
    *,
    request: AuthRequest,
    role: RoleCreate,
    roles_service: RolesService = Depends(get_roles_service),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    return await roles_service.create(role)


@router.put(
    '/{uuid}',
    summary='Update role',
    description='Update an existing role',
    response_model=RoleRead,
)
@roles_required(roles_list=['admin'])
async def update_role(
    *,
    request: AuthRequest,
    uuid: uuid.UUID,
    role: RoleUpdate,
    roles_service: RolesService = Depends(get_roles_service),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    return await roles_service.update(uuid, role)


@router.delete(
    '/{uuid}',
    summary='Delete role',
    description='Delete an existing role',
)
@roles_required(roles_list=['admin'])
async def delete_role(
    *,
    request: AuthRequest,
    uuid: UUID,
    roles_service: RolesService = Depends(get_roles_service),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    await roles_service.delete(uuid)
    return {'detail': 'Role deleted successfully'}
