import asyncio

import aio_pika
from config import settings
from on_message import on_message


async def main(loop: asyncio.AbstractEventLoop):
    connection = await aio_pika.connect_robust(
        host=settings.mq.host,
        port=settings.mq.port,
        login=settings.mq.user,
        password=settings.mq.password,
        loop=loop,
    )
    channel = await connection.channel()
    queue = await channel.declare_queue("api_notification")
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            await on_message(message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.close()
