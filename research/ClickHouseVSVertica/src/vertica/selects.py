import vertica_python
import time

connection_info = {
    'host': 'localhost',
    'port': 5440,
    'user': 'dbadmin',
    'password': '',
    'database': 'docker',
    'autocommit': True,
}
def select(query: str):
    with vertica_python.connect(**connection_info) as connection:
        start_time = time.time()
        cur = connection.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return time.time() - start_time

#Выборка всей таблицы
execution = select("SELECT * FROM movies")
print(f"Запрос всей таблицы выполнен. Время выполнения: {execution} секунд")

# Выборка уникальной записи
execution = select("SELECT * FROM movies WHERE id = 1")
print(f"Запрос уникальной записи выполнен. Время выполнения: {execution} секунд")

# Выборка нескольких записей по условию
execution = select("SELECT * FROM movies WHERE year = 2000")
print(f"Запрос нескольких записей по условию выполнен. Время выполнения: {execution} секунд")

# Выборка среднего по полю year
execution = select("SELECT AVG(year) FROM movies")
print(f"Запрос среднего по полю year выполнен. Время выполнения: {execution} секунд")

# Выборка с группировкой
execution = select("SELECT genre FROM movies GROUP BY genre")
print(f"Запрос с группировкой выполнен. Время выполнения: {execution} секунд")
