import pymongo
from pymongo.database import Database
from models import Bookmark, Like, Review, MongoUUID

class MongoLoader:
    def __init__(self, db: Database):
        self._db = db
        self._create_indexes()

    def load_ratings(self, data: list[Like]):
        mongo_data = [item.to_mongo() for item in data]
        self._base_load("likes", mongo_data)

    def load_reviews(self, data: list[Review]):
        mongo_data = [item.to_mongo() for item in data]
        self._base_load("reviews", mongo_data)

    def load_bookmarks(self, data: list[Bookmark]):
        mongo_data = [item.to_mongo() for item in data]
        self._base_load("bookmarks", mongo_data)

    def _create_indexes(self):
        self._db["likes"].create_index([("datetime", pymongo.DESCENDING)])
        self._db["reviews"].create_index([("datetime", pymongo.DESCENDING)])
        self._db["bookmarks"].create_index([("datetime", pymongo.DESCENDING)])

    def _base_load(self, collection_name: str, data):
        self._db[collection_name].insert_many([item for item in data])
