import uuid
from datetime import datetime, timedelta
from random import randint, getrandbits, choice

from models.models import NotificationEvent, Payload


async def prepare_event() -> NotificationEvent:
    event_type = ['birthday', 'registration', 'reminder', 'comment_like', 'weekly_news']
    return NotificationEvent(
        event_type=choice(event_type),
        created_dt=datetime.now(),
        schedule="0 0 * * *" if getrandbits else None,
        start_dt=datetime.now() + timedelta(days=randint(0, 10)),
        priority=randint(0, 5),
        payload=Payload(
            user_ids=[uuid.uuid4() for i in range(1, randint(1, 10))],
            movie_ids=[uuid.uuid4() for i in range(0, randint(0, 10))]
        )
    )
