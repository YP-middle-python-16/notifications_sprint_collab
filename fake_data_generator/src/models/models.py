from datetime import datetime
from typing import Any, Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Any) -> str:
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Payload(ORJSONModel):
    user_ids: list[str]
    movie_ids: Optional[list[str]]


class NotificationEvent(ORJSONModel):
    event_type: str
    created_dt: datetime
    schedule: Optional[str]
    start_dt: Optional[datetime]
    priority: int
    payload: Payload


class UserInfo(ORJSONModel):
    user_id: str
    last_name: str
    first_name: str
    email: str
    birthday_date: Optional[datetime]


class MovieInfo(ORJSONModel):
    movie_id: str
    title: str
    season: Optional[int]
    episode: Optional[int]
    release_date: Optional[datetime]
