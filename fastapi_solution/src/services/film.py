import logging
import json
import traceback

from typing import Optional

from elasticsearch import NotFoundError
from fastapi import Depends

from core.config import settings
from db.db import get_cache, get_storage
from db.base import Cache, Storage
from models.film import Film, FilmList, FilmSearchResult
from services.base import Service

logger = logging.getLogger(__name__)


class FilmService(Service):
    def __init__(self, redis: Cache, elastic: Storage):
        super().__init__(redis, elastic)
        self.redis = redis
        self.elastic = elastic
        self.cache_prefix = 'FILM'

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)
        if film.file_path:
            film.file_path = '/fileapi/api/v1/files/download-stream/'+film.file_path
        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc: Film = await self.elastic.get(doc_id=film_id)
        except NotFoundError:
            return None
        return doc

    async def get_similar_films(self, film_id: str) -> list[FilmSearchResult]:
        cache_key = f"{self.cache_prefix}:similar_films:{film_id}"
        cached_films = await self._get_list_from_cache(cache_key)

        if cached_films:
            return [
                FilmSearchResult.parse_obj(film_json)
                for film_json in cached_films
            ]

        film_response = await self.elastic.get(doc_id=film_id)

        if not film_response.genre:
            return []

        nested_query = {
            "query": {
                "nested": {
                    "path": "genre",
                    "query": {
                        "multi_match": {
                            "query": ', '.join([genre.name for genre in film_response.genre]),
                            "fields": ["genre.name"]
                        }
                    }
                }
            },
            "size": 10,
            "from": 1
        }

        try:
            response = await self.elastic.search(
                query=nested_query,
            )
            films = []
            for film_data in response:
                film = FilmSearchResult(**film_data)
                films.append(film)
            await self._put_list_to_cache(cache_key, films)
            return films
        except Exception as e:
            logger.error(e)
            return []

    async def search_films(
            self,
            query: str,
            page_number: int,
            page_size: int
    ) -> list[FilmSearchResult]:

        cache_key = f"{self.cache_prefix}:search_films:{query}:{page_number}:{page_size}"
        cached_films = await self._get_list_from_cache(cache_key)
        if cached_films:
            return [
                FilmSearchResult.parse_obj(film_json)
                for film_json in cached_films
            ]

        search_query = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "description"]
                }
            }
        }

        start_from = (page_number - 1) * page_size
        search_query["size"] = page_size
        search_query["from"] = page_number
        try:
            response = await self.elastic.search(
                query=search_query,
                from_=start_from,
                size=page_size
            )
            films = []
            for film_data in response:
                film = FilmSearchResult(**film_data)
                films.append(film)
            await self._put_list_to_cache(cache_key, films)
            return films
        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            return []

    async def get_popular_films(self, sort: Optional[str] = None) -> list[FilmList]:
        cache_key = f"{self.cache_prefix}:list_popular_films:{sort if sort else '_'}"

        cached_films = await self._get_list_from_cache(cache_key)
        if cached_films:
            return [FilmList.parse_obj(film_json) for film_json in cached_films]

        query = {
            "size": 50,
            "query": {
                "match_all": {}
            },
            "sort": [
                {
                  "imdb_rating": {
                    "order": "desc"
                  }
                }
            ],
            "from": 0
        }

        if sort:
            sort_field = sort.lstrip('-')
            sort_order = "desc" if not sort.startswith('-') else "asc"
            query["sort"].append({sort_field: sort_order})

        try:
            response = await self.elastic.search(
                query=query
            )
            films = []
            for film_data in response:
                film = FilmList(**film_data)
                films.append(film)
            await self._put_list_to_cache(cache_key, films)
            return films
        except Exception as e:
            logger.error(e)
            return []


    async def list_films(
            self,
            genre: Optional[str] = None,
            sort: Optional[str] = None
    ) -> list[FilmList]:

        cache_key = f"{self.cache_prefix}:list_films:{genre if genre else '_'}:{sort if sort else '_'}"

        cached_films = await self._get_list_from_cache(cache_key)
        if cached_films:
            return [FilmList.parse_obj(film_json) for film_json in cached_films]

        if genre:
            nested_query = {
                "query": {
                    "nested": {
                        "path": "genre",
                        "query": {
                            "multi_match": {
                                "query": genre.capitalize(),
                                "fields": ["genre.name"]
                            }
                        }
                    }
                },
                "sort": [],
                "size": 10,
                "from": 0
            }
        else:
            nested_query = {
                "query": {
                    "match_all": {}
                },
                "sort": [],
                "size": 10,
                "from": 0
            }

        if sort:
            sort_field = sort.lstrip('-')
            sort_order = "desc" if not sort.startswith('-') else "asc"
            nested_query["sort"].append({sort_field: {"order": sort_order}})
        try:
            response = await self.elastic.search(query=nested_query)

            films = []
            for film_data in response:
                film = FilmList(**film_data)
                films.append(film)
            await self._put_list_to_cache(cache_key, films)
            return films
        except Exception as e:
            traceback.print_exc()
            logger.error(e)
            return []

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        deserialized_data = json.loads(data)
        film = Film.parse_obj(deserialized_data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.uuid, film, settings.redis.redis_expire)

    async def _get_list_from_cache(self, cache_key: str) -> Optional[list]:
        try:
            data = await self.redis.get(cache_key)
            return json.loads(data) if data else None
        except Exception as e:
            logging.error(f"Error retrieving from cache: {e}")
            return None

    async def _put_list_to_cache(self, cache_key: str, data: list):
        try:
            await self.redis.set_list(cache_key, data, expire=settings.redis.redis_expire)
        except Exception as e:
            logging.error(f"Error saving to cache: {e}")


async def get_film_service(
        redis: Cache = Depends(get_cache),
        elastic: Storage = Depends(get_storage),
) -> FilmService:
    return FilmService(redis=redis.init(model=Film),
                       elastic=elastic.init(model=Film, index=settings.elastic.es_movies_index))
