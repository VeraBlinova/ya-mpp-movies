from http import HTTPStatus

import uvicorn
from httpx import Request
from starlette.responses import RedirectResponse

from api.v1.films import router as f_router
from api.v1.genres import router as g_router
from api.v1.persons import router as p_router
from core.config import settings
from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
import sentry_sdk

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
    title=settings.project.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.middleware("http")
async def handle_jwt_exceptions(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == HTTPStatus.NOT_FOUND:
        return RedirectResponse(url="/api/v1/films/popular")
    return response


app.include_router(f_router, prefix='/api/v1/films', tags=['films'])
app.include_router(g_router, prefix='/api/v1/genres', tags=['genres'])
app.include_router(p_router, prefix='/api/v1/persons', tags=['persons'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
