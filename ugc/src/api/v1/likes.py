from http import HTTPStatus
from uuid import UUID

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from services.likes_service import get_likes_service, LikesService

bp = Blueprint('likes', __name__)


@bp.route('/add/<liked_id>', methods=['POST'])
@jwt_required()
async def _add_like(liked_id: UUID, service: LikesService = get_likes_service()):
    jwt = request.headers.get('Authorization')
    doc = await service.create_like(jwt, liked_id)
    if not doc:
        return jsonify({'message': 'Cannot create like'}), HTTPStatus.BAD_REQUEST
    return jsonify({'message': f'Like with id {doc.id} created'}), HTTPStatus.CREATED


@bp.route('/remove/<like_id>', methods=['DELETE'])
@jwt_required()
async def _remove_like(like_id: UUID, service: LikesService = get_likes_service()):
    deleted = await service.delete_like(like_id)
    if not deleted:
        return jsonify({'message': 'Cannot delete like'}), HTTPStatus.BAD_REQUEST
    return jsonify({'message': f'Like with id {like_id} deleted'}), HTTPStatus.OK


@bp.route('/get/<like_id>', methods=['GET'])
@jwt_required()
async def _get_like(like_id: UUID, service: LikesService = get_likes_service()):
    doc = await service.get_like(like_id)
    if not doc:
        return jsonify({'message': 'Like not found'}), HTTPStatus.NOT_FOUND
    return jsonify(doc), HTTPStatus.OK

