from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from models.models import ORJSONModel


class DocService:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_client = mongo_client
        self.db = self.mongo_client[settings.MONGO_TEMPLATE_DB]

    async def insert(self, data: ORJSONModel, table: str):
        collection = self.db[table]
        doc_id = await collection.insert_one(data.dict())

        return doc_id.inserted_id

    async def select(self, query, table: str):
        collection = self.db[table]
        cursor = collection.find(query)

        return [document async for document in cursor]

    async def view_all(self, table: str) -> list:
        collection = self.db[table]
        cursor = collection.find()

        return [document async for document in cursor]

    async def count(self, query, table: str) -> int:
        collection = self.db[table]
        return await collection.count_documents(query)
