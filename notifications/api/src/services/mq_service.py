import logging

from aio_pika import ExchangeType, Message, connect
from core.config import settings
from models.events import BaseEvent, TypeMessage


class MQService:
    def __init__(self):
        self.connection = None

    async def init(self):
        self.connection = await connect(settings.mq.url)
        channel = await self.connection.channel()
        self.exchange = await channel.declare_exchange(
            settings.mq.exchange, ExchangeType.HEADERS
        )

        queue = await channel.declare_queue("api_notification")
        await queue.bind(
            exchange=self.exchange,
            routing_key="",
            arguments={"x-match": "all", "type": TypeMessage.EMAIL.value},
        )
        await queue.bind(
            exchange=self.exchange,
            routing_key="",
            arguments={"x-match": "all", "type": TypeMessage.SMS.value},
        )
        await queue.bind(
            exchange=self.exchange,
            routing_key="",
            arguments={"x-match": "all", "type": TypeMessage.PUSH.value},
        )

        async def on_message(message):
            async with message.process():
                logging.info("Received message:", message.body.decode())

        await queue.consume(on_message)

        return self

    async def send_to_mq(self, event: BaseEvent):
        async with self.connection:
            event_data = event.dict()
            message = Message(
                body=str(event_data).encode(),
                headers={"type": event.notification_type.value},
            )
            await self.exchange.publish(message, routing_key=self.exchange.name)


async def get_mq_service() -> MQService:
    return await MQService().init()
