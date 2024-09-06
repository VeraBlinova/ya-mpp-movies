from http import HTTPStatus
from uuid import UUID

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from services.reviews_service import get_review_service, ReviewService

bp = Blueprint('reviews', __name__)


@bp.route('/add', methods=['POST'])
@jwt_required()
async def _add_review(service: ReviewService = get_review_service()):
    movie_id = request.args.get('movie_id')
    text = request.args.get('text')
    access_token = request.headers.get('Authorization')
    doc = await service.create_review(access_token, movie_id, text)
    if not doc:
        return jsonify({'message': 'Cannot create review'}), HTTPStatus.BAD_REQUEST
    return jsonify({'message': f'Review with id {doc.id} created'}), HTTPStatus.CREATED


@bp.route('/remove/<review_id>', methods=['DELETE'])
@jwt_required()
async def _remove_review(review_id: UUID, service: ReviewService = get_review_service()):
    deleted = await service.delete_review(review_id)
    if not deleted:
        return jsonify({'message': 'Cannot delete review'}), HTTPStatus.BAD_REQUEST
    return jsonify({'message': f'Review with id {review_id} deleted'}), HTTPStatus.OK


@bp.route('/get/<review_id>', methods=['GET'])
@jwt_required()
async def _get_review(review_id: UUID, service: ReviewService = get_review_service()):
    doc = await service.get_review(review_id)
    if not doc:
        return jsonify({'message': 'Review not found'}), HTTPStatus.NOT_FOUND
    return jsonify(doc.dict())


@bp.route('/update', methods=['PUT'])
@jwt_required()
async def _update_review(service: ReviewService = get_review_service()):
    review_id = request.args.get('id')
    text = request.args.get('text')
    updated = await service.update_review(review_id, text)
    if not updated:
        return jsonify({'message': 'Cannot update review'}), HTTPStatus.BAD_REQUEST
    return jsonify({'message': f'Review with id {review_id} updated'}), HTTPStatus.OK


@bp.route('/get_reviews', methods=['GET'])
@jwt_required()
async def _get_user_reviews(service: ReviewService = get_review_service()):
    access_token = request.headers.get('Authorization')
    docs = await service.get_user_reviews(access_token)
    if not docs:
        return {'message': 'No reviews found'}, HTTPStatus.NOT_FOUND
    return jsonify([doc.dict() for doc in docs]), HTTPStatus.OK
