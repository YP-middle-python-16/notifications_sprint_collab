from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME = 'Fake data generator'
    NOTIFICATION_HOST: str = Field(env="NOTIFICATION_HOST", default="0.0.0.0")
    NOTIFICATION_PORT: str = Field(env="NOTIFICATION_PORT", default=8000)
    SEND_EVENT_ENDPOINT: str = Field(env="SEND_EVENT_ENDPOINT", default='/event')
    REPEAT_TASK_EVERY_SECONDS: int = 5


settings = Settings()
