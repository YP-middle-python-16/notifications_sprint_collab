from fastapi import APIRouter, Depends

from core.config import settings
from models.models import StatusMessage, NotificationEvent, NotificationStatus
from services.doc_service import DocService
from services.service_locator import get_storage_service

router = APIRouter()


@router.post(
    '/',
    response_model=StatusMessage,
    summary='Notification event registration endpoint',
    description='Notification event registration endpoint',
)
async def insert_notification_event(event: NotificationEvent,
                                    storage_service: DocService = Depends(get_storage_service)) -> StatusMessage:

    event_id = await storage_service.insert(event, settings.MONGO_TABLE_RAW)

    return StatusMessage(head='status', body=f'Event {event_id} was registered')


@router.post(
    '/status/{event_id}',
    response_model=NotificationStatus,
    summary='Update notification event delivery status',
    description='Update notification event delivery status',
)
async def update_notification_status(event_id: str, status: str,
                                     storage_service: DocService = Depends(get_storage_service)) -> NotificationStatus:
    msg = NotificationStatus(id=event_id, status=status)
    await storage_service.insert(msg, settings.MONGO_TABLE_STATUS)

    return msg
