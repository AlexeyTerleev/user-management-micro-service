import aio_pika
import bson
from datetime import datetime

from app.config import settings


class RabbitMQService:

    async def get_connection(self):
        return await aio_pika.connect_robust(settings.rabbit_mq.get_url())

    async def send_reset_password_message(self, email, url):
        connection = await self.get_connection()
        async with connection:

            channel = await connection.channel()
            queue = await channel.declare_queue(settings.rabbit_mq.RESET_PASSWORD_QUEUE, durable=True, arguments={"x-queue-type": "quorum"})

            message = {
                "email": email,
                "reset_password_url": url,
                "timestamp": datetime.now()
            }

            bson_message = bson.BSON.encode(message)

            await channel.default_exchange.publish(
                aio_pika.Message(
                    bson_message,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                ),
                routing_key=queue.name,
            )
