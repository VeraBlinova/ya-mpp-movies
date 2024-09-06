import logging
from contextlib import asynccontextmanager

import uvicorn
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from fastapi_limiter.depends import RateLimiter

from fastapi_oauth2.middleware import OAuth2Middleware
from fastapi_oauth2.router import router as oauth2_router
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from fastapi_limiter import FastAPILimiter

from redis.asyncio import Redis

from api.v1.history import router as history_router
from api.v1.jwt import router as jwt_router
from api.v1.roles import router as roles_router
from api.v1.users import router as users_router
from api.v1.oauth import router as oauth_router
from auth import get_current_user_global
from core.config import settings
from core.logger import LOGGING
from core.oauth import oauth2_config
from db import redis_db
from tracer.tracer import configure_tracer

import sentry_sdk



@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_db.redis = Redis.from_url(settings.redis.url, decode_responses=True)

    await FastAPILimiter.init(redis=redis_db.redis)
    yield

    await FastAPILimiter.close()
    await redis_db.redis.close()

sentry_sdk.init(
    dsn="https://d9afa0bac80ea937ce26d819f8efb9fe@o4506961499521024.ingest.us.sentry.io/4506961501945856",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)



app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    docs_url='/authapi/openapi',
    openapi_url='/authapi/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return ORJSONResponse(
        status_code=exc.status_code, content={'detail': exc.message}
    )


@app.middleware('http')
async def before_request(request: Request, call_next):
    response = await call_next(request)
    if settings.request_id_needed:
        request_id = request.headers.get('X-Request-Id')
        if not request_id:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={'detail': 'X-Request-Id is required'}
            )
    return response


app.include_router(jwt_router, prefix='/authapi/api/v1/jwt', tags=['jwt'],
                   dependencies=[Depends(RateLimiter(times=settings.request_limit_per_minute, minutes=1))])
app.include_router(
    history_router, prefix='/authapi/api/v1/history', tags=['history'],
    dependencies=[Depends(RateLimiter(times=settings.request_limit_per_minute, minutes=1))]
)
app.include_router(
    users_router, prefix='/authapi/api/v1/users', tags=['users'],
    dependencies=[Depends(RateLimiter(times=settings.request_limit_per_minute, minutes=1))]
)
app.include_router(
    roles_router,
    prefix='/authapi/api/v1/roles',
    tags=['roles'],
    dependencies=[Depends(get_current_user_global),
                  Depends(RateLimiter(times=settings.request_limit_per_minute, minutes=1))],
)

app.include_router(oauth2_router)
app.include_router(oauth_router,prefix='/authapi/api/v1')
app.add_middleware(OAuth2Middleware, config=oauth2_config)

if settings.tracer.enable:
    configure_tracer()
    FastAPIInstrumentor.instrument_app(app)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.app_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=settings.debug,
    )
