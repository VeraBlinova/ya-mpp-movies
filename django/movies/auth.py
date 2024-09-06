import http
import json
import logging
from enum import StrEnum, auto

import requests
from jose import jwt

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()

logger = logging.getLogger(__name__)


class Roles(StrEnum):
    ADMIN = auto()


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        url = settings.AUTH_API_LOGIN_URL
        try:
            payload = {'login': username, 'password': password}
            headers = {'X-Request-Id' : '27290d28d5c38da315a78399d71fc20b'}
            response = requests.post(url, data=json.dumps(payload),headers=headers)
            if response.status_code != http.HTTPStatus.OK:
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f'Authentication error: {e}')
            return None

        jwt_tokens = response.json()
        access_token = jwt_tokens['access_token']

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'X-Request-Id' : '27290d28d5c38da315a78399d71fc20b'
        }
        resp = requests.get(
            settings.AUTH_API_PROFILE_URL,
            headers=headers,
        )

        try:
            user_data = resp.json()
            user, created = User.objects.get_or_create(
                id=user_data['id'],
            )
            user.email = user_data['login']
            user.first_name = user_data.get('first_name')
            user.last_name = user_data.get('last_name')
            user_role = jwt.decode(access_token, settings.AUTH_JWT_SECRET_KEY)[
                'role'
            ]
            user.is_admin = user_role == Roles.ADMIN
            user.is_active = user_data.get('is_active')
            user.set_unusable_password()
            user.save()
        except Exception as e:
            logger.error(f'Exception: {str(e)}')
            return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
