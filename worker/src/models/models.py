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
    header: str
    template: str
    body: Optional[dict]


class NotificationEvent(ORJSONModel):
    receivers_list: list[str]
    sender: str
    event_type: str
    transport: Optional[list[str]]
    priority: int
    created_dt: Optional[str]
    schedule: Optional[str]
    start_date: Optional[str]
    payload: Payload


class EnrichedNotification(ORJSONModel):
    notification_id: str
    priority: str
    type: str
    transport: dict


class NotificationStatus(ORJSONModel):
    _id: str
    status: str


class NotificationEmail(ORJSONModel):
    address: str
    subject: str
    message: str
