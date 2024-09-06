from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from models.models import Event
from services.kafka_service import KafkaService, get_kafka_service

bp = Blueprint('events', __name__)


@bp.get('/ping')
@jwt_required()
def ping():
    return 'pong'


@bp.post('/save')
@jwt_required()
async def save(kafka_service: KafkaService = get_kafka_service()):
    request_data = request.get_json()
    event = Event.model_validate(request_data)

    kafka_service.save(
        topic='events',
        key=event.key.encode('UTF-8'),
        value=event.value.encode('UTF-8'),
    )
    return jsonify({'message': 'Event saved'}), HTTPStatus.OK
