import logging

import uvicorn
from api.v1.events import router as events_router
from api.v1.template import router as template_router
from core.config import settings
from core.logger import LOGGING
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    docs_url="/Napi/openapi",
    openapi_url="/Napi/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(events_router, prefix="/Napi/v1", tags=["events"])

app.include_router(template_router, prefix="/Napi/v1", tags=["templates"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.app_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
        reload=True,
    )
