from typing import Any, Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Any) -> str:
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class SMS(ORJSONModel):
    number: str
    message: str


class Email(ORJSONModel):
    address: str
    sender: str
    header: str
    message: str


class Push(ORJSONModel):
    device: str
    message: str


class Transport(ORJSONModel):
    sms: Optional[SMS]
    email: Optional[Email]
    push: Optional[Push]


class FinishedNotification(ORJSONModel):
    _id: str
    type: Optional[str]
    transport: Transport


class Payload(ORJSONModel):
    header: str
    template: str
    body: Optional[dict]


class RawNotification(ORJSONModel):
    receivers_list: list[str]
    sender: str
    event_type: str
    transport: Optional[list[str]]
    priority: int
    created_dt: Optional[str]
    schedule: Optional[str]
    start_date: Optional[str]
    payload: Payload
