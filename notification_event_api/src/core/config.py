from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = Field(env='PROJECT_NAME', default='NOTIFICATION_API')

    # mongo settings
    MONGO_CONNECTION: str = Field(env="MONGO_CONNECTION", default="mongodb://localhost:27017/")
    MONGO_DB: str = Field(env="MONGO_DB", default='NOTIFICATIONS')

    MONGO_TABLE_RAW: str = Field(env="MONGO_TABLE_RAW", default='raw_notifications')
    MONGO_TABLE_ENRICHED: str = Field(env="MONGO_TABLE_ENRICHED", default='enriched_notifications')
    MONGO_TABLE_STATUS: str = Field(env="MONGO_TABLE_STATUS", default='notification_status')

    RABBIT_MQ_HOST: str = Field(env="RABBIT_MQ_HOST", default='127.0.0.1')
    RABBIT_MQ_PORT: int = Field(env="RABBIT_MQ_PORT", default=5672)
    RABBIT_MQ_USER: str = Field(env="RABBIT_MQ_USER", default='guest')
    RABBIT_MQ_PASSWORD: str = Field(env="RABBIT_MQ_PASSWORD", default='guest')
    RABBIT_MQ_CONN_TIMEOUT: int = Field(env="RABBIT_MQ_CONN_TIMEOUT", default=10)

    CHECK_HEADERS: bool = Field(env="CHECK_HEADERS", default=False)


settings = Settings()
