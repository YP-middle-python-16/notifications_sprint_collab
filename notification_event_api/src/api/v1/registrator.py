from fastapi import APIRouter, Depends

from core.config import settings
from core.logger import logger
from models.models import (
    StatusMessage,
    RawNotificationEvent,
    NotificationStatus,
    NotificationEvent,
)
from services.doc_service import DocService
from services.service_locator import get_storage_service

router = APIRouter()


@router.post(
    '/',
    response_model=StatusMessage,
    summary='Notification event registration endpoint',
    description='Notification event registration endpoint',
)
async def insert_notification_event(event: RawNotificationEvent,
                                    storage_service: DocService = Depends(get_storage_service)) -> StatusMessage:
    result_notification = NotificationEvent(**event.to_dict())
    await storage_service.insert(result_notification, settings.MONGO_TABLE_RAW)
    logger.info(f'event {result_notification.notification_id} has been inserted to MondoDB with data: {event.dict()}')
    return StatusMessage(head='status', body=f'Event {result_notification.notification_id} was registered')


@router.post(
    '/status/{notification_id}',
    response_model=NotificationStatus,
    summary='Update notification event delivery status',
    description='Update notification event delivery status',
)
async def update_notification_status(notification_id: str, status: str,
                                     storage_service: DocService = Depends(get_storage_service)) -> NotificationStatus:
    msg = NotificationStatus(notification_id=notification_id, status=status)
    await storage_service.insert(msg, settings.MONGO_TABLE_STATUS)
    logger.info(f'event {notification_id} has been updated with status={status} to MondoDB')

    return msg
