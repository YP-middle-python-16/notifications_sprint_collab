import logging

import pika
import uvicorn
from pymongo import MongoClient
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
@backoff.on_exception(backoff.expo, ServerSelectionTimeoutError, max_tries=3)
async def startup():
    # create mongo connection
    mongo.mongo_client = MongoClient(settings.MONGO_CONNECTION, serverSelectionTimeoutMS=1)
    mongo.mongo_client.server_info()
    # create rabbit_mq connection
    rabbit_mq.connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBIT_MQ_HOST))


# Подключаем роутер к серверу, указав префикс /v1/****
# Теги указываем для удобства навигации по документации
app.include_router(events.router, prefix="/api/v1/event", tags=["Event"])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
