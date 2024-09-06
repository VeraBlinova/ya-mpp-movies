from kafka import KafkaProducer

from core.config import settings


class KafkaService:
    def __init__(self, topic: str = 'events'):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.kafka.producer,
        )
        self.topic = settings.kafka.topic

    def save(self, topic, value, key=None):
        self.producer.send(topic, value=value, key=key)
        self.producer.flush()   # TODO: maybe remove


def get_kafka_service():
    return KafkaService()
