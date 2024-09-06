import logging

from clickhouse_driver import Client
from main_generator import generate
from data_generator import init_db

client = Client(host="clickhouse")


def ch_load():
    while True:
        data = ", ".join([f"({d['id']}, '{d['title']}', {d['year']}, '{d['genre']}')" for d in generate()])
        client.execute(f"INSERT INTO movies_db.movies (id, title, year, genre) VALUES {data}")
        logging.info("Inserted %s rows", len(data))


if __name__ == "__main__":
    init_db()
    ch_load()
