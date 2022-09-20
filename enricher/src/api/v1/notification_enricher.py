import aiohttp
from fastapi import APIRouter, logger

from core.config import settings
from models.models import RawNotification, FinishedNotification

router = APIRouter()


@router.post('/{notification_id}',
             response_model=FinishedNotification,
             summary='Enrich notification',
             description='Enrich notification')
async def enrich(notification_id: str, notification: RawNotification) -> FinishedNotification:
    # todo тут надо словить body из пэйлоада, receivers_list по транспорту (будем считать, что для одного получателя)
    #  и по нему запросить инфу, формируя конечный context dict

    try:
        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as session:
            url = f'http://{settings.NOTIFICATION_HOST.rstrip("/")}:{settings.NOTIFICATION_PORT}/{settings.SEND_EVENT_ENDPOINT.lstrip("/")}'  # noqa E501
            async with session.post(url, data=event.json()) as response:
                response.raise_for_status()
    except Exception as e:
        logger.logger.error('!!!!!!!!!!!!!!!!' + str(e))
        raise

    return event
