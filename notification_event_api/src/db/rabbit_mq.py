from typing import Optional


from pika import BlockingConnection

rabbit_mq_connection: Optional[BlockingConnection] = None


# Функция понадобится при внедрении зависимостей
async def get_rabbit_mq_connection() -> BlockingConnection:
    return rabbit_mq_connection
