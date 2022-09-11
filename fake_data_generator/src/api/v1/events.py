import uuid
from datetime import datetime, timedelta
from random import choice, getrandbits, randint

from fastapi import APIRouter
from models.models import NotificationEvent, Payload

EVENT_TYPE = ['birthday', 'registration', 'reminder', 'comment_like', 'weekly_news']

router = APIRouter()


@router.post("/",
             response_model=NotificationEvent,
             summary="Send event to make notification",
             description="Send event to make notification")
async def send_notification_event() -> NotificationEvent:
    return NotificationEvent(
        event_type=choice(EVENT_TYPE),
        created_dt=datetime.now(),
        schedule="0 0 * * *" if getrandbits else None,
        start_dt=datetime.now() + timedelta(days=randint(0, 10)),
        priority=randint(0, 5),
        payload=Payload(
            user_ids=[uuid.uuid4() for i in range(1, randint(1, 10))],
            movie_ids=[uuid.uuid4() for i in range(0, randint(0, 10))]
        )
    )
