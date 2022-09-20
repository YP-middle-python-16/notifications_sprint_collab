from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    PROJECT_NAME = 'Enricher'
    FAKE_GENERATOR_API_HOST: str = Field(env='FAKE_GENERATOR_API_HOST', default='localhost')
    FAKE_GENERATOR_API_PORT: str = Field(env='FAKE_GENERATOR_API_PORT', default=8004)
    USER_INFO_ENDPOINT: str = Field(env='USER_INFO_ENDPOINT', default='/api/v1/info/auth/users')
    CONTENT_INFO_ENDPOINT: str = Field(env='CONTENT_INFO_ENDPOINT', default='/api/v1/info/auth/movies')


settings = Settings()
