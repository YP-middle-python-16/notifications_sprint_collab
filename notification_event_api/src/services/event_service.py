from aio_pika import RobustConnection, Message
from async_property import async_property

from models.models import EnrichedNotification


class EventService:
    def __init__(self, rabbitmq_conn: RobustConnection):
        self.rabbitmq_conn = rabbitmq_conn
        self._channel = None

    @async_property
    async def channel(self):
        if not self._channel:
            self._channel = await self.rabbitmq_conn.channel()

        return self._channel

    async def send_message(self, notification: EnrichedNotification, queue_name: str, encoding: str = 'utf-8'):
        await self.channel.declare_queue(queue_name)
        await self.channel.default_exchange.publish(
            Message(body=notification.json().encode(encoding)),
            routing_key=queue_name,
        )
