import logging

import vertica_python

from main_generator import generate
from data_generator import connection_info, init_db


def vertica_load():
    while True:
        data = generate()
        with vertica_python.connect(**connection_info) as connection:
            cur = connection.cursor()
            execute_many_query = f"INSERT INTO movies (title, year, genre) VALUES (:title, :year, :genre)"
            cur.executemany(execute_many_query, data)
            logging.info("Inserted %s rows", len(data))


if __name__ == "__main__":
    init_db()
    vertica_load()
