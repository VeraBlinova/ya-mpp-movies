from datetime import datetime
from random import randint
from uuid import UUID, uuid4

from faker import Faker
from models import Bookmark, Like, Review


faker = Faker()
def generate_uuids(count) -> list[UUID]:
    return [uuid4() for _ in range(count)]


def _get_random_uuid(ids: list[UUID]) -> UUID:
    return ids[randint(0, len(ids) - 1)]


def generate_ratings(count: int, user_ids: list[UUID], movie_ids: list[UUID]) -> list[Like]:
    ratings = []
    for i in range(count):
        id = uuid4()
        user_id = _get_random_uuid(user_ids)
        liked_id = _get_random_uuid(movie_ids)
        ratings.append(Like(id=id, user_id=user_id, liked_id=liked_id, datetime=datetime.utcnow(), rate=randint(0, 10)))
    return ratings


def generate_reviews(count, user_ids: list[UUID], movie_ids: list[UUID]) -> list[Review]:
    reviews = []
    for i in range(count):
        id = uuid4()
        user_id = _get_random_uuid(user_ids)
        movie_id = _get_random_uuid(movie_ids)
        reviews.append(
            Review(id=id, user_id=user_id, movie_id=movie_id, datetime=datetime.utcnow(), text=faker.text())
        )
    return reviews


def generate_bookmarks(count, user_ids: list[UUID], movie_ids: list[UUID]) -> list[Bookmark]:
    bookmarks = []
    for i in range(count):
        id = uuid4()
        user_id = _get_random_uuid(user_ids)
        movie_id = _get_random_uuid(movie_ids)
        bookmarks.append(Bookmark(id=id,user_id=user_id, movie_id=movie_id, datetime=datetime.utcnow()))
    return bookmarks
