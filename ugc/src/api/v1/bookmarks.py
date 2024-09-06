import logging
from http import HTTPStatus
from uuid import UUID

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from services.bookmark_service import get_bookmark_service, BookmarkService

bp = Blueprint('bookmarks', __name__)


@bp.route('/add/<movie_id>', methods=['POST'])
@jwt_required()
async def _add_bookmark(movie_id: UUID, service: BookmarkService = get_bookmark_service()):
    access_token = request.headers.get('Authorization')
    doc = await service.create_bookmark(access_token, movie_id)
    if not doc:
        return jsonify({'message': 'Cannot create bookmark'}), HTTPStatus.BAD_REQUEST
    return jsonify({'message': f'Bookmark with id {doc.id} created'}), HTTPStatus.CREATED


@bp.route('/remove/<bookmark_id>', methods=['DELETE'])
@jwt_required()
async def _remove_bookmark(bookmark_id: UUID, service: BookmarkService = get_bookmark_service()):
    deleted = await service.delete_bookmark(bookmark_id)
    if not deleted:
        return jsonify({'message': 'Cannot delete bookmark'}), HTTPStatus.BAD_REQUEST
    return jsonify({'message': f'Bookmark with id {bookmark_id} deleted'}), HTTPStatus.OK


@bp.route('/get/<bookmark_id>', methods=['GET'])
@jwt_required()
async def _get_bookmark(bookmark_id: UUID, service: BookmarkService = get_bookmark_service()):
    doc = await service.get_bookmark(bookmark_id)
    if not doc:
        return jsonify({'message': 'Bookmark not found'}), HTTPStatus.NOT_FOUND
    return jsonify(doc.dict()), HTTPStatus.OK


@bp.route('/get_bookmarks', methods=['GET'])
@jwt_required()
async def _get_user_bookmarks(service: BookmarkService = get_bookmark_service()):
    access_token = request.headers.get('Authorization')
    docs = await service.get_user_bookmarks(access_token)
    if not docs:
        return {'message': 'No bookmarks found'}, HTTPStatus.NOT_FOUND
    return jsonify([doc.dict() for doc in docs]), HTTPStatus.OK
