from typing import Any, Optional
from uuid import uuid4

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v: Any, *, default: Any) -> str:
    return orjson.dumps(v, default=default).decode()


class ORJSONModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps

    def to_dict(self):
        return self.dict()


class StatusMessage(ORJSONModel):
    head: str
    body: str


class Payload(ORJSONModel):
    header: str
    template: str
    body: Optional[dict]


class RawNotificationEvent(ORJSONModel):
    receivers_list: list[str]
    sender: str
    event_type: str
    transport: Optional[list[str]]
    priority: str
    created_dt: Optional[str]
    schedule: Optional[str]
    start_date: Optional[str]
    payload: Payload


class NotificationEvent(RawNotificationEvent):
    notification_id: str = Field(default_factory=uuid4)

    def to_dict(self):
        data = self.dict()
        data["notification_id"] = str(self.notification_id)
        return data


class EnrichedNotification(ORJSONModel):
    notification_id: str
    priority: str
    type: str
    transport: dict


class NotificationStatus(ORJSONModel):
    notification_id: str
    status: str
