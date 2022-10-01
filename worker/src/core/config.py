from logging import config as logging_config

# from core.logger import LOGGING
from pydantic import BaseSettings, Field


# Применяем настройки логирования
# logging_config.dictConfig(LOGGING)


class RabbitPriorityQueue(BaseSettings):
    exchange: str = Field(env='RABBIT_PRIORITY_QUEUE_EXCHANGE', default="hight_priority")
    exchange_type: str = Field(env='RABBIT_PRIORITY_QUEUE_EXCHANGE_TYPE', default="direct")
    queue: str = Field(env='RABBIT_PRIORITY_QUEUE', default="hight_priority")
    durable: str = Field(env='RABBIT_PRIORITY_QUEUE_DURABLE', default="True")


class RabbitQueue(BaseSettings):
    exchange: str = Field(env='RABBIT_QUEUE_EXCHANGE', default="low_priority")
    exchange_type: str = Field(env='RABBIT_QUEUE_EXCHANGE_TYPE', default="direct")
    queue: str = Field(env='RABBIT_QUEUE', default='low_priority')
    durable: str = Field(env='RABBIT_QUEUE_DURABLE', default="True")


class Settings(BaseSettings):
    RABBIT_HOST: str = Field(env="RABBIT_HOST", default='127.0.0.1')
    RABBIT_PORT: int = Field(env="RABBIT_PORT", default=5672)
    RABBIT_USER: str = Field(env="RABBIT_USER", default='guest')
    RABBIT_PASSWORD: str = Field(env="RABBIT_PASSWORD", default='guest')
    RABBIT_CONN_TIMEOUT: int = Field(env="RABBIT_CONN_TIMEOUT", default=10)

    rabbit_hight_priority: RabbitPriorityQueue = RabbitPriorityQueue()
    rabbit_low_priority: RabbitQueue = RabbitQueue()

    EMAIL_SENDER_TYPE: str = Field(env="EMAIL_SENDER_TYPE", default="fake")
    SMS_SENDER_TYPE: str = Field(env="SMS_SENDER_TYPE", default="fake")
    PUSH_SENDER_TYPE: str = Field(env="PUSH_SENDER_TYPE", default="fake")

    NOTIFICATION_HOST: str = Field(env="NOTIFICATION_HOST", default="localhost")
    NOTIFICATION_PORT: str = Field(env="NOTIFICATION_PORT", default="8000")
    SEND_EVENT_ENDPOINT: str = Field(env="SEND_EVENT_ENDPOINT", default="/api/v1/event/status")



settings = Settings()
