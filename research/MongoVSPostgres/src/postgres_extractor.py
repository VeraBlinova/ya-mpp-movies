from uuid import UUID

from psycopg2.extensions import connection


class PostgresExtractor:
    def __init__(self, conn: connection):
        self.conn = conn

    def get_ratings(self, user_id: UUID = None, limit: int = None) -> list[list]:
        return self._get_all_base("likes", user_id, limit)

    def get_reviews(self, user_id: UUID = None, limit: int = None) -> list[list]:
        return self._get_all_base("reviews", user_id, limit)

    def get_all_likes(self, user_id: UUID = None, liked_id: UUID = None, limit: int = None) -> list[list]:
        if user_id or liked_id:
            where_query = "WHERE "
        else:
            where_query = ""

        if user_id:
            user_id_str = str(user_id)
            where_query += f"user_id = '{user_id_str}'"

        if liked_id:
            liked_id_str = str(liked_id)
            if user_id:
                where_query += " AND "
            where_query += f"liked_id = '{liked_id_str}'"

        limit_query = ""
        if limit:
            limit_query = f" LIMIT {limit}"

        with self.conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM likes " f"{where_query}" f"ORDER BY datetime DESC {limit_query}")
            return cursor.fetchall()

    def get_bookmarks(self, user_id: UUID = None, limit: int = None) -> list[list]:
        return self._get_all_base("bookmarks", user_id, limit)

    def get_likes(self, liked_id: UUID = None, reverse_sort: bool = False, limit: int = None) -> list[list]:
        return self._base_get_likes(True, liked_id, reverse_sort=reverse_sort, limit=limit)

    def get_dislikes(self, liked_id: UUID = None, reverse_sort: bool = False, limit: int = None) -> list[list]:
        return self._base_get_likes(False, liked_id, reverse_sort=reverse_sort, limit=limit)

    def get_movies_with_top_ratings(self, reverse_sort: bool = False, limit: int = None) -> list[list]:
        limit_query = ""
        if limit:
            limit_query = f" LIMIT {limit}"

        sort_order = "DESC"
        if reverse_sort:
            sort_order = "ASC"

        with self.conn.cursor() as cursor:
            cursor.execute(
                f"SELECT liked_id, avg(rate) FROM likes "
                f"GROUP BY liked_id ORDER BY avg {sort_order} {limit_query}"
            )
            return cursor.fetchall()

    def _get_all_base(self, table_name: str, user_id: UUID = None, limit: int = None) -> list[list]:
        where_query = ""
        if user_id:
            user_id_str = str(user_id)
            where_query = f"WHERE user_id = '{user_id_str}'"

        limit_query = ""
        if limit:
            limit_query = f" LIMIT {limit}"

        with self.conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name} " f"{where_query}" f"ORDER BY datetime DESC {limit_query}")
            return cursor.fetchall()

    def _base_get_likes(self, is_liked: bool, liked_id: UUID, reverse_sort: bool = False, limit: int = None):
        is_liked_condition = "0"
        if is_liked:
            is_liked_condition = "10"

        where_query = f"WHERE rate = {is_liked_condition}"
        if liked_id:
            liked_id_str = str(liked_id)
            where_query = f" AND '{liked_id_str}'"

        limit_query = ""
        if limit:
            limit_query = f" LIMIT {limit}"

        sort_order = "DESC"
        if reverse_sort:
            sort_order = "ASC"

        with self.conn.cursor() as cursor:
            cursor.execute(
                f"SELECT liked_id, count(liked_id) FROM likes "
                f"{where_query} "
                f"GROUP BY liked_id ORDER BY count {sort_order} {limit_query}"
            )
            return cursor.fetchall()
