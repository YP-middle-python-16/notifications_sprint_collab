import datetime
from typing import Any, Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Any) -> str:
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class StatusMessage(ORJSONModel):
    head: str
    body: str


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


class EnrichedNotification(ORJSONModel):
    _id: str
    priority: int
    type: str
    transport: dict


class NotificationStatus(ORJSONModel):
    _id: str
    status: str
