from fastapi import APIRouter
from models.models import NotificationEvent
from services.event import prepare_event

router = APIRouter()


@router.post("/",
             response_model=NotificationEvent,
             summary="Send event to make notification",
             description="Send event to make notification")
async def send_notification_event() -> NotificationEvent:
    return await prepare_event()
