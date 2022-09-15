from typing import Optional

import motor.motor_asyncio

mongo_client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None


# Функция понадобится при внедрении зависимостей
async def get_mongo_client() -> motor.motor_asyncio.AsyncIOMotorClient:
    return mongo_client
