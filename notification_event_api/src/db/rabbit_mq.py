from typing import Optional

from aio_pika import RobustConnection

rabbit_mq_connection: Optional[RobustConnection] = None


# Функция понадобится при внедрении зависимостей
async def get_rabbit_mq_connection() -> RobustConnection:
    return rabbit_mq_connection
