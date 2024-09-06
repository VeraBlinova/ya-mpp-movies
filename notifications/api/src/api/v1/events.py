from fastapi import APIRouter, Depends, status
from models.events import CustomEvent, NewMovieEvent, RegistrationEvent
from services.mq_service import MQService, get_mq_service

router = APIRouter()


@router.post("/new_user")
async def new_user(event: RegistrationEvent, mq: MQService = Depends(get_mq_service)):
    await mq.send_to_mq(event)
    return status.HTTP_200_OK


@router.post("/new_movie")
async def new_movie(event: NewMovieEvent, mq: MQService = Depends(get_mq_service)):
    await mq.send_to_mq(event)
    return status.HTTP_200_OK


@router.post("/new_event")
async def new_movie(event: CustomEvent, mq: MQService = Depends(get_mq_service)):
    await mq.send_to_mq(event)
    return status.HTTP_200_OK
