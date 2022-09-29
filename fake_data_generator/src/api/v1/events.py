import uuid
from datetime import datetime, timedelta
from random import choice, getrandbits, randint

import aiohttp
from fastapi import APIRouter, logger
from fastapi_utils.tasks import repeat_every

from core.config import settings
from models.models import RawNotificationEvent, Payload
from . import fake

EVENT_TYPE = ['birthday', 'registration', 'reminder', 'comment_like', 'weekly_news']
TRANSPORT = ['sms', 'push', 'email']

router = APIRouter()


@router.post("/",
             response_model=RawNotificationEvent,
             summary="Send event to make notification",
             description="Send event to make notification")
@repeat_every(seconds=settings.REPEAT_TASK_EVERY_SECONDS)
async def send_notification_event() -> RawNotificationEvent:
    scheduled = getrandbits(1)
    event = RawNotificationEvent(
        receivers_list=[str(uuid.uuid4()) for i in range(1, randint(1, 10))],
        sender=f'{fake.word()}@yandex.ru',
        event_type=choice(EVENT_TYPE),
        transport=[TRANSPORT[i] for i in range(randint(0, len(TRANSPORT) - 1))],
        created_dt=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
        schedule='0 0 * * *' if scheduled else None,
        start_dt=(datetime.now() + timedelta(days=randint(0, 10))).strftime(
            '%Y-%m-%d %H:%M:%S.%f') if scheduled else None,
        priority=randint(0, 5),
        payload=Payload(header=' '.join([fake.word() for i in range(randint(1, 5))]),
                        template=fake.word(),
                        body={
                            'movie_ids': [str(uuid.uuid4()) for i in range(0, randint(0, 10))],
                            'timezone': 'Europe/Moscow',
                        })
    )
    try:
        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as session:
            url = f'http://{settings.NOTIFICATION_HOST.rstrip("/")}:{settings.NOTIFICATION_PORT}/{settings.SEND_EVENT_ENDPOINT.lstrip("/")}'  # noqa E501
            async with session.post(url, data=event.json()) as response:
                response.raise_for_status()
    except Exception as e:
        logger.logger.error('!!!!!!!!!!!!!!!!' + str(e))
        raise

    return event
