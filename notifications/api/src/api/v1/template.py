from uuid import UUID

from fastapi import APIRouter, Depends, status
from models.notifications import Content
from services.template import ContentService, get_template_service

router = APIRouter()


@router.get("/template/{uuid}")
async def template_get(
    *,
    uuid: UUID,
    content_service: ContentService = Depends(get_template_service),
):

    return await content_service.get(uuid)


@router.post("/template/")
async def template_create(
    *,
    uuid: UUID,
    content: str,
    content_service: ContentService = Depends(get_template_service),
):
    model_obj = Content(content_id=uuid, content=content)
    await content_service.add(model_obj)
    return status.HTTP_200_OK


@router.delete("/template/{uuid}")
async def template_delete(
    *,
    uuid: UUID,
    content_service: ContentService = Depends(get_template_service),
):
    result = await content_service.delete(uuid)
    if result:
        return status.HTTP_200_OK
    else:
        return status.HTTP_404_NOT_FOUND
