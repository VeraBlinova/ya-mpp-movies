import pytest
import requests
from http import HTTPStatus

API_URL = 'http://127.0.0.1/eventapi/save'
LOGIN_URL = 'http://127.0.0.1/authapi/api/v1/jwt/login'


@pytest.mark.asyncio
@pytest.fixture(scope='module')
def get_access_token():
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


def test_save_event_unauthorized():
    response = requests.post(API_URL, json={'key': 'test', 'value': 'event'})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_save_event_authorized(get_access_token):
    headers = {'Authorization': f'Bearer {get_access_token}'}
    response = requests.post(
        API_URL, headers=headers, json={'key': 'test', 'value': 'event'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Event saved'}


def test_save_event_with_invalid_data(get_access_token):
    headers = {'Authorization': f'Bearer {get_access_token}'}
    invalid_data = {'invalid_key': 'abc', 'another_invalid_key': '123'}
    response = requests.post(API_URL, headers=headers, json=invalid_data)
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


def test_save_event_missing_data(get_access_token):
    headers = {'Authorization': f'Bearer {get_access_token}'}
    incomplete_data = {'key': 'test_key'}
    response = requests.post(API_URL, headers=headers, json=incomplete_data)
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
