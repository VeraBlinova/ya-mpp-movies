import pytest
import asyncio
import requests

LOGIN_URL = 'http://127.0.0.1/authapi/api/v1/jwt/login'


@pytest.mark.asyncio
@pytest.fixture(scope='session')
async def get_access_token():
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'login': 'mail@mail.ru',
        'password': '123qwe',
    }

    response = requests.post(
        LOGIN_URL,
        headers=headers,
        json=json_data,
    )
    return response.json()['access_token']