import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.files import router as files_router
from core.config import settings
from core.logger import LOGGING
from dependencies.main import setup_dependencies
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
    title=settings.project_name,
    description=settings.project_description,
    docs_url='/fileapi/openapi',
    openapi_url='/fileapi/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(
    files_router, prefix='/fileapi/api/v1/files', tags=['files']
)

setup_dependencies(app)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=settings.app_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=settings.debug,
    )
