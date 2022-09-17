from functools import lru_cache

from fastapi import Depends

from db.async_message_queue import AsyncMessageQueue
from db.async_storage import AsyncStorage
from db.rabbit_mq import get_rabbit_mq_connection
from db.mongo import get_mongo_client
from services.doc_service import DocService
from services.event_service import EventService


@lru_cache()
def get_event_service(
        rabbitmq_conn: AsyncMessageQueue = Depends(get_rabbit_mq_connection),
) -> EventService:
    return EventService(rabbitmq_conn=rabbitmq_conn)


@lru_cache()
def get_storage_service(
        mongo_client: AsyncStorage = Depends(get_mongo_client)
) -> DocService:
    return DocService(mongo_client=mongo_client)
