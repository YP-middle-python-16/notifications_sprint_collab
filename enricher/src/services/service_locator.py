from functools import lru_cache

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from db.mongo import get_mongo_client
from services.doc_service import DocService


@lru_cache()
def get_storage_service(
        mongo_client: AsyncIOMotorClient = Depends(get_mongo_client)
) -> DocService:
    return DocService(mongo_client=mongo_client)
