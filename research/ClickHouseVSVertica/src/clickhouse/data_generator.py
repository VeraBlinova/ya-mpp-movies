import time
from multiprocessing import Pool

from clickhouse_driver import Client
from faker import Faker

from main_generator import generate, BATCHES, BATCH_SIZE, RECORDS_TO_INSERT

fake = Faker()
client = Client(host="clickhouse")
def init_db():
    client.execute('CREATE DATABASE IF NOT EXISTS movies_db')

    client.execute('CREATE TABLE IF NOT EXISTS movies_db.movies (id Int64, title String, year Int32, genre String) '
                   'Engine=MergeTree() ORDER BY id')


def mult_insert_data(i: int):
    print(f"Этап {i + 1}/{BATCHES}")
    ch_data = ", ".join([f"({d['id']}, '{d['title']}', {d['year']}, '{d['genre']}')" for d in generate()])
    client.execute(f'INSERT INTO movies_db.movies (id, title, year, genre) VALUES {ch_data}')
    print(f"Этап {i + 1}/{BATCHES}: вставлено {BATCH_SIZE * (i + 1)}/{RECORDS_TO_INSERT}")


if __name__ == "__main__":
    init_db()
    start_time = time.time()
    pool = Pool(processes=12)
    pool.map(mult_insert_data, range(BATCHES))
    pool.close()
    pool.join()
    execution = time.time() - start_time
    print(f"Запрос множественной вставки выполнен. Время выполнения: {execution} секунд")







