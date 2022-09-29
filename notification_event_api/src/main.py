import uuid
import logging

import aio_pika
import uvicorn
import motor.motor_asyncio
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.middleware import is_valid_uuid4

from api.v1 import registrator, transmitter
from core.config import settings
from core.logger import configure_logging, LOGGING, logger
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
@backoff.on_exception(backoff.expo, Exception, max_time=60)
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
app.include_router(registrator.router, prefix='/api/v1/event', tags=['event_registration'])
app.include_router(transmitter.router, prefix='/api/v1/delivery', tags=['delivery_info'])


@app.middleware('http')
async def request_processing(request: Request, call_next):
    # check header
    request_id = request.headers.get("X-Request-Id")
    if settings.CHECK_HEADERS and not request_id:
        raise RuntimeError("request id is required")
    response = await call_next(request)
    # add tag for logs
    custom_logger = logging.LoggerAdapter(
        logger, extra={'tag': 'ugc_api', 'request_id': request_id}
    )
    custom_logger.info(request)
    return response

# Добавим middleware для работы с X-Request-Id (https://github.com/snok/asgi-correlation-id)
app.add_middleware(
    CorrelationIdMiddleware,
    header_name="X-Request-ID",
    generator=lambda: uuid.uuid4().hex,
    validator=is_valid_uuid4,
    transformer=lambda a: a,
)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
