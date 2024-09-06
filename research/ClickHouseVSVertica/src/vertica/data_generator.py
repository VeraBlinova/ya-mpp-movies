import time
from multiprocessing import Pool
import vertica_python
from faker import Faker
from dataclasses import dataclass

from main_generator import generate, BATCHES, BATCH_SIZE, RECORDS_TO_INSERT

fake = Faker()

@dataclass
class Movie:
    id: int
    title: str
    year: int
    genre: str

connection_info = {
    'host': 'vertica',
    'port': 5433,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
}

def init_db():
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        cursor.execute("""  
        CREATE TABLE IF NOT EXISTS movies (
            id IDENTITY,
            title VARCHAR(256) NOT NULL,
            year INTEGER NOT NULL,
            genre VARCHAR(256) NOT NULL
        );
        """)

def mult_insert_data(i: int):
    print(f"Этап {i + 1}/{BATCHES}")
    vertica_data = generate()
    with vertica_python.connect(**connection_info) as connection:
        cur = connection.cursor()
        execute_many_query = f"INSERT INTO movies (title, year, genre) VALUES (:title, :year, :genre)"
        cur.executemany(execute_many_query, vertica_data)
    print(f"Этап {i + 1}/{BATCHES}: вставлено {BATCH_SIZE * (i + 1)}/{RECORDS_TO_INSERT}")


if __name__ == "__main__":
    init_db()
    start_time = time.time()
    print("Start generate data")
    pool = Pool(processes=12)
    pool.map(mult_insert_data, range(BATCHES))
    pool.close()
    pool.join()
    end_time = time.time()
    print(f"Запрос вставки выполнен. Время выполнения: {end_time - start_time} секунд")