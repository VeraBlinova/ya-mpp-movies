from clickhouse_driver import Client
from kafka import KafkaConsumer
import os
import backoff
import logging
from logging import StreamHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sh = StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s')
sh.setFormatter(formatter)

logger.addHandler(sh)


CLICK_SERVER = os.environ.get('CLICK_SERVER', 'clickhouse') 
CLICK_CLUSTER = os.environ.get('CLICK_CLUSTER', 'ugc') 
CLICK_DB = os.environ.get('CLICK_DB', 'ugc') 
CLICK_TABLE = os.environ.get('CLICK_TABLE', 'events') 
KAFKA_PRODUCER=os.environ.get('KAFKA_PRODUCER','kafka-0')
KAFKA_TOPIC=os.environ.get('KAFKA_TOPIC','events')


@backoff.on_exception(backoff.constant, ConnectionError, interval=3, max_tries=20)
def click_connect():
    client = Client(host=CLICK_SERVER)
    return client

def init_clickhouse():
    client = click_connect()
    client.execute(f'CREATE DATABASE IF NOT EXISTS {CLICK_DB} ON CLUSTER {CLICK_CLUSTER}')
    client.execute(f'CREATE TABLE IF NOT EXISTS {CLICK_DB}.{CLICK_TABLE} ON CLUSTER {CLICK_CLUSTER} (key String, value String) Engine=MergeTree() ORDER BY key')
    client.disconnect()

def init_kafka():
    consumer = KafkaConsumer(KAFKA_TOPIC,
                             group_id= 'etl' ,
                             bootstrap_servers=[KAFKA_PRODUCER],
                             enable_auto_commit=False)
    logger.info(f'Connection to kafka: {consumer.bootstrap_connected()}')
    logger.info(f'Subsribe on topic: {consumer.subscription()}')
    logger.info(f'Partition on topic: {consumer.partitions_for_topic(KAFKA_TOPIC)}')
    return consumer

if __name__ == '__main__':
    init_clickhouse()
    while True:
        click = click_connect()
        kafka = init_kafka()
        while True:
            try:
                message = kafka.poll(timeout_ms=1000, max_records=1000)
                if message:
                    data = [[rec.key.decode(),rec.value.decode()] for rec in list(message.values())[0] ]
                    logger.info(f'Insert {len(data)} rows')
                    click.execute(f'INSERT INTO {CLICK_DB}.{CLICK_TABLE} values ', data)
                    kafka.commit()
            except Exception as e:
                logger.error(e)
                break
        logger.error('Reconnect....')

