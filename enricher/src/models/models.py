from typing import Any, Optional, Union, Dict

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
    device: Optional[str]
    message: str


class Transport(ORJSONModel):
    sms: Optional[SMS]
    email: Optional[Email]
    push: Optional[Push]


class Payload(ORJSONModel):
    header: str
    template: str
    body: Optional[dict]


class RawNotification(ORJSONModel):
    receivers_list: list[str]
    sender: str
    event_type: str
    transport: Optional[str]
    priority: int
    created_dt: Optional[str]
    schedule: Optional[str]
    start_date: Optional[str]
    payload: Payload


class FinalNotification(ORJSONModel):
    _id: str
    priority: int
    type: str = 'transactional'
    transport: Dict[str, list]
