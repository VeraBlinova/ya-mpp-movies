from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from db.postgres import get_db_session
from decorators import jwt_required
from services.history import get_history_service
from services.jwt import JWTService, get_jwt_service

router = APIRouter()


@router.post(
    '/login-history',
    summary='User Login History',
    description='Retrieve the login history of the currently logged-in user.',
)
@jwt_required
async def login_history(
    jwt_service: JWTService = Depends(get_jwt_service),
    db_session: AsyncSession = Depends(get_db_session),
    limit: int = Query(default=10, description="Limit number of records"),
    offset: int = Query(default=0, description="Offset for records"),
):
    current_user = await jwt_service.get_user()
    current_history = get_history_service(current_user, db_session)
    result = await current_history.get(limit=limit, offset=offset)
    return result
