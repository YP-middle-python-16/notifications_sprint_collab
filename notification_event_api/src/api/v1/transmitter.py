from fastapi import APIRouter, Depends

from core.logger import logger
from models.models import StatusMessage, EnrichedNotification
from services.event_service import EventService
from services.service_locator import get_event_service

router = APIRouter()


@router.post(
    '/',
    response_model=StatusMessage,
    summary='Send notification to message broker',
    description='Send notification to message broker',
)
async def send_notification_to_broker(event: EnrichedNotification,
                                      broker_service: EventService = Depends(get_event_service)) -> StatusMessage:
    await broker_service.send_message(event, str(event.priority))
    logger.info(f'event {event._id} has been sent to RabbitMQ')
    return StatusMessage(head='status', body=f'Event {event._id} has been sent')
