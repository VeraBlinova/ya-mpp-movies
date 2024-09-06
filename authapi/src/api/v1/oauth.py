from fastapi_oauth2.security import OAuth2
from fastapi import Depends,APIRouter,Request, Header
from models.user import UserCreate
from services.jwt import JWTService, get_jwt_service
from services.users import UserService, get_user_service
from services.history import get_history_service
from services.roles import RolesService, get_roles_service
from services.social import SocialService,get_social_service
from sqlmodel.ext.asyncio.session import AsyncSession
from db.postgres import get_db_session
from typing import Annotated

router = APIRouter()

oauth2 = OAuth2()

@router.get("/oauth")
async def login(
    request: Request,
    _: str = Depends(oauth2), 
    jwt_service: JWTService = Depends(get_jwt_service),
    user_service: UserService = Depends(get_user_service),
    roles_service: RolesService = Depends(get_roles_service),
    social_Service: SocialService = Depends(get_social_service),
    user_agent: Annotated[str | None, Header()] = None,
    db_session: AsyncSession = Depends(get_db_session)
    ):
    curr_user = await social_Service.get(request.user['provider'],request.user['id'])
    if curr_user:
        user = await user_service.get_by_id(curr_user[0].user_id)
    else:
        roles = await roles_service.get_multi()
        for role in roles:
            if role.description == "subscriber":
                role_id = role.id
        if request.user.get('default_email'):
            login = request.user['default_email']
        else:
            login = request.user['provider']+'_'+request.user['id']
        data = {
            "login": login,
            "password": request.user['psuid'],
            "first_name": request.user['first_name'],
            "last_name": request.user['last_name'],
            "is_active": True,
            "role_id": role_id
        }
        user_data = UserCreate(**data)
        user = await user_service.create(user_data)
        await social_Service.add(user.id,request.user['provider'],request.user['id'])
    tokens = await jwt_service.create_tokens(user.login,user.role.name)
    current_history = get_history_service(user.login, db_session)
    await current_history.update(user_agent)
    return tokens




