import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import notification_enricher
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/v1/openapi",
    openapi_url="/api/v1/openapi.json",
    default_response_class=ORJSONResponse,
)
app.include_router(notification_enricher.router, prefix="/api/v1/notification", tags=["Notification"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8006,
    )
