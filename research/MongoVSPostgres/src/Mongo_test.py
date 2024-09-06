from timeit import timeit
from functools import partial
from pymongo import MongoClient

from data_generator import generate_ratings, generate_reviews, generate_bookmarks, generate_uuids
from mongo_loader import MongoLoader
from mongo_extractor import MongoExtractor

MONGO_DB_CONNECTION_STRING = "mongodb://localhost:27017/"
mongo_db = MongoClient(MONGO_DB_CONNECTION_STRING)["test_db"]

BATCH_SIZE = 100000

REQUESTS_COUNT = 5

# Количество запрашиваемых данных.
LIMIT = 1000

# Количество данных для тестирования.
USERS_COUNT = 10000 # Активные пользователи.
MOVIES_COUNT = 100000
MOVIE_LIKES_COUNT = USERS_COUNT * 30 # Допускаем, что каждый активный юзер оценил в среднем 30 фильмов.
REVIEWS_COUNT = MOVIES_COUNT * 2 # Допускаем, что в среднем фильм получил по три ревью.
REVIEW_LIKES_COUNT = REVIEWS_COUNT * 3 # Предполагаем, что в среднем ревью получают по 3 лайков или дизлайков.
BOOKMARKS_COUNT = USERS_COUNT * 10 # В среднем у каждого активного юзера по 10 закладок.

# Общие ID пользователей, фильмов и ревью.
user_ids = generate_uuids(USERS_COUNT)
movie_ids = generate_uuids(MOVIES_COUNT)
review_ids = generate_uuids(REVIEWS_COUNT)

# Генерируем данные с использованием общих ID.
reviews = generate_reviews(REVIEWS_COUNT, user_ids, movie_ids)
bookmarks = generate_bookmarks(BOOKMARKS_COUNT, user_ids, movie_ids)
movie_likes = generate_ratings(MOVIE_LIKES_COUNT, user_ids, movie_ids)
review_likes = generate_ratings(REVIEW_LIKES_COUNT, user_ids, review_ids)

def load(method, data):
    chunks = [data[i:i + BATCH_SIZE] for i in range(0, len(data), BATCH_SIZE)]
    for chunk in chunks:
        method(chunk)

mi = MongoLoader(mongo_db)
load(mi.load_ratings, movie_likes)
load(mi.load_ratings, review_likes)
load(mi.load_reviews, reviews)
load(mi.load_bookmarks, bookmarks)


me = MongoExtractor(mongo_db)
print("get_ratings")
print(round(timeit(partial(me.get_ratings, limit=LIMIT, user_id=user_ids[0]), number=REQUESTS_COUNT) / REQUESTS_COUNT, 3))
print("get_reviews")
print(round(timeit(partial(me.get_reviews, limit=LIMIT), number=REQUESTS_COUNT) / REQUESTS_COUNT, 3))
print("get_rates")
print(round(timeit(partial(me.get_rates, limit=LIMIT), number=REQUESTS_COUNT) / REQUESTS_COUNT, 3))
print("get_bookmarks")
print(round(timeit(partial(me.get_bookmarks, limit=LIMIT), number=REQUESTS_COUNT) / REQUESTS_COUNT, 3))

print("get_likes")
print(round(timeit(partial(me.get_likes, limit=LIMIT), number=REQUESTS_COUNT) / REQUESTS_COUNT, 3))
print("get_dislikes")
print(round(timeit(partial(me.get_dislikes, limit=LIMIT), number=REQUESTS_COUNT) / REQUESTS_COUNT, 3))
print("get_movies_with_top_ratings")
print(round(timeit(partial(me.get_movies_with_top_ratings, limit=LIMIT), number=REQUESTS_COUNT) / REQUESTS_COUNT, 3))