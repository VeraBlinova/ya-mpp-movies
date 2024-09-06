from uuid import UUID

import pymongo
from bson.son import SON
from pymongo.cursor import Cursor
from pymongo.database import Database
from models import MongoUUID


class MongoExtractor:
    def __init__(self, db: Database):
        self._db = db
        self._likes = db["likes"]
        self._reviews = db["reviews"]
        self._bookmarks = db["bookmarks"]

    def get_reviews(self, user_id: UUID = None, limit: int = None) -> list[dict]:
        return MongoExtractor._get_all_base(self._reviews, user_id, limit)

    def get_ratings(self, user_id: UUID = None, limit: int = None) -> list[dict]:
        return MongoExtractor._get_all_base(self._likes, user_id, limit)

    def get_rates(self, user_id: UUID = None, review_id: UUID = None, limit: int = None):
        query = {}
        if user_id:
            query["user_id"] = user_id
        if review_id:
            query["liked_id"] = review_id
        data = self._likes.find(query).sort("datetime", pymongo.DESCENDING).allow_disk_use(True)
        return MongoExtractor._get_data_list(data, limit)

    def get_bookmarks(self, user_id: UUID = None, limit: int = None) -> list[dict]:
        return MongoExtractor._get_all_base(self._bookmarks, user_id, limit)

    def get_likes(self, liked_id: UUID = None, limit: int = None) -> list[dict]:
        pipeline = _build_get_ratings_with_value_pipeline(10, liked_id)
        data = self._likes.aggregate(pipeline, allowDiskUse=True)
        return MongoExtractor._get_data_list(data, limit)

    def get_dislikes(self, liked_id: UUID = None, limit: int = None) -> list[dict]:
        pipeline = _build_get_ratings_with_value_pipeline(0, liked_id)
        data = self._likes.aggregate(pipeline, allowDiskUse=True)
        return MongoExtractor._get_data_list(data, limit)

    def get_movies_with_top_ratings(self, reverse_sort: bool = False, limit: int = None) -> list[dict]:
        if reverse_sort:
            sort_order = pymongo.ASCENDING
        else:
            sort_order = pymongo.DESCENDING

        pipeline = [
            {"$group": {"_id": "$liked_id", "rate": {"$avg": "rate"}}},
            {"$sort": SON([("rate", sort_order)])},
        ]
        data = self._likes.aggregate(pipeline, allowDiskUse=True)
        return MongoExtractor._get_data_list(data, limit)


    @staticmethod
    def _get_data_list(data_collection: Cursor, limit: int = None):
        data_list = []
        if limit is None:
            limit = 999999999999
        i = 1
        for item in data_collection:
            data_list.append(item)
            i += 1
            if i > limit:
                break
        return data_list

    @staticmethod
    def _get_all_base(collection, user_id: UUID = None, limit: int = None) -> list[dict]:
        query = None
        if user_id:
            query = {
                "user_id": MongoUUID(user_id).id,
            }
        data = collection.find(query).sort("datetime", pymongo.DESCENDING).allow_disk_use(True)
        return MongoExtractor._get_data_list(data, limit)


def _build_get_ratings_with_value_pipeline(value: int, liked_id: UUID = None):
    pipeline = [
        {"$match": {"rate": {"$eq": value}}},
        {"$group": {"_id": "$liked_id", "count": {"$count": {}}}},
        {"$sort": SON([("count", pymongo.DESCENDING)])},
    ]
    if liked_id:
        pipeline[0]["$match"]["liked_id"] = MongoUUID(liked_id).id  # type: ignore
    return pipeline
