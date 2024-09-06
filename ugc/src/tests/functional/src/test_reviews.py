import asyncio
from http import HTTPStatus
from uuid import uuid4
import aiohttp

import pytest
import requests

from ugc.src.tests.functional.helper import get_id
REVIEWS_URL = 'http://127.0.0.1/eventapi/v1/reviews'

review_data = {'movie_id': uuid4(), 'text': 'text'}



@pytest.mark.asyncio
@pytest.fixture()
async def create_review(get_access_token):
    headers = {'Authorization': f'Bearer {get_access_token}'}
    movie_id = review_data['movie_id']
    text = review_data['text']
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{REVIEWS_URL}/add?movie_id={movie_id}&text={text}", headers=headers) as response:
            review_data['id'] = get_id((await response.json())['message'])
            return response


@pytest.mark.asyncio
async def test_create_review(create_review):
    review = await create_review

    assert review.status == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_get_review(create_review, get_access_token):
    await create_review
    headers = {'Authorization': f'Bearer {get_access_token}'}
    review_id = review_data['id']
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{REVIEWS_URL}/get/{review_id}", headers=headers) as response:
            assert response.status == HTTPStatus.OK
            json = await response.json()
            assert json['movie_id'] == review_data['movie_id']
            assert json['text'] == review_data['text']


@pytest.mark.asyncio
async def test_get_wrong_review(create_review, get_access_token):
    await create_review
    headers = {'Authorization': f'Bearer {await get_access_token}'}
    response = requests.get(f"{REVIEWS_URL}/get/{uuid4()}", headers=headers)

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_all_reviews(create_review, get_access_token):
    async with aiohttp.ClientSession() as session:
        reviews_tasks = [create_review for _ in range(5)]
        await asyncio.gather(*reviews_tasks)

        headers = {'Authorization': f'Bearer {get_access_token}'}
        async with session.get(f"{REVIEWS_URL}/get_reviews", headers=headers) as response:
            assert response.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_delete_review(create_review, get_access_token):
    review = await create_review
    headers = {'Authorization': f'Bearer {get_access_token}'}
    review_id = review_data['id']
    response = requests.delete(f"{REVIEWS_URL}/remove/{review_id}", headers=headers, )

    assert response.status_code == HTTPStatus.OK
