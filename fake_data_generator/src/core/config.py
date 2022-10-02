from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME = 'Fake data generator'
    NOTIFICATION_HOST: str = Field(env="NOTIFICATION_HOST", default="localhost")
    NOTIFICATION_PORT: str = Field(env="NOTIFICATION_PORT", default=8000)
    SEND_EVENT_ENDPOINT: str = Field(env="SEND_EVENT_ENDPOINT", default='/api/v1/event/')
    REPEAT_TASK_EVERY_SECONDS: int = 5

    MONGO_CONNECTION: str = Field(env="MONGO_CONNECTION", default="mongodb://localhost:27017/")
    MONGO_TEMPLATE_DB: str = Field(env='MONGO_TEMPLATE_DB', default='TEMPLATES')
    MONGO_TEMPLATE_TABLE: str = Field(env='MONGO_TEMPLATE_TABLE', default='TEMPLATES')


settings = Settings()
