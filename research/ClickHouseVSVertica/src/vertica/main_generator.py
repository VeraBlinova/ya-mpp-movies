from dataclasses import dataclass

from faker import Faker

RECORDS_TO_INSERT = 10000000
BATCH_SIZE = RECORDS_TO_INSERT // 500  # Рекомендованное значение от 1000 до 10000, согласно документации CH.
BATCHES = RECORDS_TO_INSERT // BATCH_SIZE

fake = Faker()
@dataclass
class Movie:
    id: int
    title: str
    year: int
    genre: str


def generate() -> list[dict[str, int | str]]:
    data = []
    for _ in range(BATCH_SIZE):
        data.append(
            Movie(fake.random_int(min=1, max=RECORDS_TO_INSERT), fake.word(), fake.random_int(min=1900, max=2022),
                  fake.word()).__dict__)
    return data
