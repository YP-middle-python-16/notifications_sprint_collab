from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

router = APIRouter()


@router.post("/auth/users",
             response_class=ORJSONResponse,
             summary="Send event to make notification",
             description="Send event to make notification")
async def send_user_info(user_id: str):
    result = await event_service.send_message(event_message)

    return ORJSONResponse({"status": "success"})
