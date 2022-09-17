from asyncio.exceptions import TimeoutError
import logging

import aio_pika
import uvicorn
import motor.motor_asyncio
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from pymongo.errors import ServerSelectionTimeoutError

from core.config import settings
from core.logger import configure_logging, LOGGING
from db import mongo, rabbit_mq
import backoff

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/v1/openapi',
    openapi_url='/api/v1/openapi.json',
    default_response_class=ORJSONResponse,
    on_startup=[configure_logging],
)


@app.on_event('startup')
@backoff.on_exception(backoff.expo, (ServerSelectionTimeoutError, TimeoutError), max_tries=3)
async def startup():
    # create mongo connection
    mongo.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_CONNECTION,
                                                                serverSelectionTimeoutMS=1)
    await mongo.mongo_client.server_info()
    # create rabbit_mq connection
    rabbit_mq.rabbit_mq_connection = await aio_pika.connect_robust(host=settings.RABBIT_MQ_HOST,
                                                                   port=settings.RABBIT_MQ_PORT,
                                                                   login=settings.RABBIT_MQ_USER,
                                                                   password=settings.RABBIT_MQ_PASSWORD,
                                                                   timeout=settings.RABBIT_MQ_CONN_TIMEOUT)


# Подключаем роутер к серверу, указав префикс /v1/****
# Теги указываем для удобства навигации по документации
app.include_router(events.router, prefix="/api/v1/event", tags=["NotificationEvent"])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
