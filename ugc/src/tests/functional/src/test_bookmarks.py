import asyncio
from http import HTTPStatus
from uuid import uuid4
import aiohttp

import pytest
import pytest_asyncio
import requests

from ugc.src.tests.functional.helper import get_id

BOOKMARKS_URL = 'http://127.0.0.1/eventapi/v1/bookmarks'

bookmark_data = {'movie_id': uuid4()}


@pytest.mark.asyncio
@pytest.fixture()
async def create_bookmark(get_access_token):
    headers = {'Authorization': f'Bearer {get_access_token}'}
    movie_id = bookmark_data['movie_id']
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BOOKMARKS_URL}/add/{movie_id}", headers=headers) as response:
            bookmark_data['id'] = get_id((await response.json())['message'])
            return response


@pytest.mark.asyncio
async def test_create_bookmark(create_bookmark):
    bookmark = await create_bookmark
    assert bookmark.status == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_get_bookmark(create_bookmark, get_access_token):
    await create_bookmark
    headers = {'Authorization': f'Bearer {get_access_token}'}
    id = bookmark_data['id']
    movie_id = bookmark_data['movie_id']
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BOOKMARKS_URL}/get/{id}", headers=headers) as response:
            assert response.status == HTTPStatus.OK
            assert (await response.json())['movie_id'] == movie_id


@pytest.mark.asyncio
async def test_get_wrong_bookmark(create_bookmark, get_access_token):
    await create_bookmark
    headers = {'Authorization': f'Bearer {await get_access_token}'}
    response = requests.get(f"{BOOKMARKS_URL}/get/{uuid4()}", headers=headers)

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_all_bookmarks(create_bookmark, get_access_token):
    async with aiohttp.ClientSession() as session:
        bookmark_tasks = [create_bookmark for _ in range(5)]
        await asyncio.gather(*bookmark_tasks)

        headers = {'Authorization': f'Bearer {get_access_token}'}
        async with session.get(f"{BOOKMARKS_URL}/get_bookmarks", headers=headers) as response:
            assert response.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_delete_bookmark(create_bookmark, get_access_token):
    bookmark = await create_bookmark
    headers = {'Authorization': f'Bearer {get_access_token}'}
    id = bookmark_data['id']
    response = requests.delete(f"{BOOKMARKS_URL}/remove/{id}", headers=headers, )

    assert response.status_code == HTTPStatus.OK
