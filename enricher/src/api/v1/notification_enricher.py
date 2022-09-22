from fastapi import APIRouter, Depends

from models.models import RawNotification, FinalNotification
from services.message_collector import MessageCollector
from services.service_locator import get_storage_service
from services.storage.base import BaseStorage

router = APIRouter()


@router.post('/{notification_id}',
             response_model=FinalNotification,
             summary='Enrich notification',
             description='Enrich notification')
async def enrich(notification_id: str,
                 notification: RawNotification,
                 type: str = 'transactional',
                 storage_service: BaseStorage = Depends(get_storage_service)) -> FinalNotification:
    msg_collector = MessageCollector(notification_id=notification_id,
                                     notification=notification,
                                     type=type,
                                     storage_service=storage_service)

    return await msg_collector.get_final_notifications()
