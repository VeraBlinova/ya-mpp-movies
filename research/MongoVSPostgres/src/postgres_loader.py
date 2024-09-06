import csv
import io
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

from psycopg2.extensions import connection
from models import BaseData, Bookmark, Like, Review


def _convert_model_list_to_dict_list(data: list[BaseData]):
    """
    Преобразует список объектов с объектами Pydantic в список словарей
    """
    output_dict_list: list[dict] = []
    for item in data:
        dict_object = item.dict()
        # Добавляем поле с id, так как его изначально нет.
        dict_object["id"] = uuid4()
        output_dict_list.append(dict_object)
    return output_dict_list


def get_columns(data: list[BaseData]):
    prepared_data = _convert_model_list_to_dict_list(data)
    columns = prepared_data[0].keys()
    return columns


class PostgresLoader:
    def __init__(self, conn: connection):
        self.conn = conn

    def load_ratings(self, data: list[Like]):
        self._save_to_table("likes", data)

    def load_review(self, data: list[Review]):
        self._save_to_table("reviews", data)

    def load_bookmarks(self, data: list[Bookmark]):
        self._save_to_table("bookmarks", data)

    def _save_to_table(self, table_name: str, data: list[BaseData]):
        columns = get_columns(data)
        columns_str = ", ".join(columns)

        inserted_data = []
        for item in data:
            row = []
            for column in columns:
                row.append(f"'{item.dict()[column]}'")
            inserted_data.append(f"({', '.join(map(str, row))})")

        inserted_data_str = ", ".join(inserted_data)
        with self.conn.cursor() as cursor:
            cursor.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES {inserted_data_str};")