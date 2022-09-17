from fastapi import APIRouter, Depends

from core.config import settings
from models.models import StatusMessage, NotificationEvent
from services.doc_service import DocService
from services.service_locator import get_storage_service

router = APIRouter()


@router.post(
    '/',
    response_model=StatusMessage,
    summary='Notification event registration endpoint',
    description='Notification event registration endpoint',
)
async def insert_notification_vent(event: NotificationEvent,
                                   storage_service: DocService = Depends(get_storage_service)) -> StatusMessage:
    await storage_service.insert(event.dict(), settings.MONGO_TABLE_BOOKMARK)

    return StatusMessage(head='status', body='all ok')
