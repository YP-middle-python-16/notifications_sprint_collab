import backoff
import motor.motor_asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import notification_enricher
from core.config import settings
from db import mongo

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/v1/openapi",
    openapi_url="/api/v1/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
@backoff.on_exception(backoff.expo, Exception, max_time=60)
async def startup():
    # create mongo connection
    mongo.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_CONNECTION,
                                                                serverSelectionTimeoutMS=1)
    await mongo.mongo_client.server_info()


app.include_router(notification_enricher.router, prefix="/api/v1/notification", tags=["Notification"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8006,
    )
