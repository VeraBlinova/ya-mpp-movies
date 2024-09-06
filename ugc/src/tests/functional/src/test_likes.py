import asyncio
from http import HTTPStatus
from uuid import uuid4
import aiohttp

import pytest
import pytest_asyncio
import requests

from ugc.src.tests.functional.helper import get_id

LIKES_URL = 'http://127.0.0.1/eventapi/v1/bookmarks'

likes_data = {'movie_id': uuid4()}


@pytest.mark.asyncio
@pytest.fixture()
async def create_like(get_access_token):
    headers = {'Authorization': f'Bearer {get_access_token}'}
    movie_id = likes_data['movie_id']
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{LIKES_URL}/add/{movie_id}", headers=headers) as response:
            likes_data['id'] = get_id((await response.json())['message'])
            return response


@pytest.mark.asyncio
async def test_create_like(create_like):
    like = await create_like

    assert like.status == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_get_like(create_like, get_access_token):
    await create_like
    headers = {'Authorization': f'Bearer {get_access_token}'}
    movie_id = likes_data['movie_id']
    like_id = likes_data['id']
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{LIKES_URL}/get/{like_id}", headers=headers) as response:
            assert response.status == HTTPStatus.OK
            assert response.json()['movie_id'] == movie_id


@pytest.mark.asyncio
async def test_get_wrong_like(create_like, get_access_token):
    await create_like
    headers = {'Authorization': f'Bearer {await get_access_token}'}
    response = requests.get(f"{LIKES_URL}/get/{uuid4()}", headers=headers)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_delete_like(create_like, get_access_token):
    await create_like
    headers = {'Authorization': f'Bearer {get_access_token}'}
    like_id = likes_data['id']
    response = requests.delete(f"{LIKES_URL}/remove/{like_id}", headers=headers, )

    assert response.status_code == HTTPStatus.OK
