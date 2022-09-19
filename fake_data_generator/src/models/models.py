from typing import Any, Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Any) -> str:
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class NotificationEvent(ORJSONModel):
    receivers_list: list[str]
    sender: str
    event_type: str
    transport: Optional[list[str]]
    priority: int
    created_dt: Optional[str]
    schedule: Optional[str]
    start_date: Optional[str]
    payload: dict


class UserInfo(ORJSONModel):
    user_id: str
    last_name: str
    first_name: str
    email: str
    birthday_date: Optional[str]


class MovieInfo(ORJSONModel):
    movie_id: str
    title: str
    season: Optional[int]
    episode: Optional[int]
    release_date: Optional[str]
