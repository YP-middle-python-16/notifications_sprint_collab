from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from models.models import ORJSONModel


class DocService:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_client = mongo_client
        self.db = self.mongo_client[settings.MONGO_DB]

    async def insert(self, data: ORJSONModel, table: str):
        collection = self.db[table]
        doc_id = await collection.insert_one(data.dict()).inserted_id

        return doc_id

    async def select(self, query, table: str):
        collection = self.db[table]
        result = await collection.find(query)
        return list(result)

    async def view_all(self, table: str) -> list:
        collection = self.db[table]
        result = await collection.find()
        return list(result)

    async def count(self, query, table: str) -> int:
        collection = self.db[table]
        return await collection.count_documents(query)
