import time
from clickhouse_driver import Client

client = Client(host="localhost")

# Выборка всей таблицы
start_time = time.time()
client.execute("SELECT * FROM movies_db.movies")
execution = time.time() - start_time
print(f"Запрос всей таблицы выполнен. Время выполнения: {execution} секунд")

# Выборка уникальной записи
start_time = time.time()
client.execute("SELECT * FROM movies_db.movies WHERE id = 1")
execution = time.time() - start_time
print(f"Запрос уникальной записи выполнен. Время выполнения: {execution} секунд")

# Выборка нескольких записей по условию
start_time = time.time()
client.execute("SELECT * FROM movies_db.movies WHERE year = 2000")
execution = time.time() - start_time
print(f"Запрос нескольких записей по условию выполнен. Время выполнения: {execution} секунд")

# Выборка среднего по полю year
start_time = time.time()
client.execute("SELECT AVG(year) FROM movies_db.movies")
execution = time.time() - start_time
print(f"Запрос среднего по полю year выполнен. Время выполнения: {execution} секунд")

# Выборка с группировкой
start_time = time.time()
client.execute("SELECT genre FROM movies_db.movies GROUP BY genre")
execution = time.time() - start_time
print(f"Запрос с группировкой выполнен. Время выполнения: {execution} секунд")

