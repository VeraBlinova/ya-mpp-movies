import http
import json
import logging
from os import environ

import requests

logger = logging.getLogger(__name__)


def get_email(user_id=None):
    login = environ["WORKER_LOGIN"]
    password = environ["WORKER_PASS"]
    login_url = environ["WORKER_LOGIN_URL"]
    profile_url = environ["WORKER_PROFILE_URL"]
    try:
        payload = {"login": login, "password": password}
        headers = {"X-Request-Id": "27290d28d5c38da315a78399d71fc20b"}
        response = requests.post(login_url, data=json.dumps(payload), headers=headers)
        if response.status_code != http.HTTPStatus.OK:
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Authentication error: {e}")
        return None

    jwt_tokens = response.json()
    access_token = jwt_tokens["access_token"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "X-Request-Id": "27290d28d5c38da315a78399d71fc20b",
    }
    url = f"{profile_url}/{user_id}"
    resp = requests.get(
        url,
        headers=headers,
    )

    try:
        user_data = resp.json()
        user_email = user_data["login"]
    except Exception as e:
        logger.error(f"Exception: {str(e)}")
        return False

    return user_email
