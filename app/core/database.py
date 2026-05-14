from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient
import os
from app.core.config import settings

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):

        uri = settings.MONGO_URI
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client.get_database(settings.DATABASE_NAME)
        print("Conexión exitosa a MongoDB Atlas")

    async def close(self):
        if self.client:
            self.client.close()


    async def save_if_new(self, corte_dict: dict, custom_key: str):

        collection = self.db.cortes
    
        try:
            await collection.update_one(
                {"_id": custom_key},
                {
                    "$set": corte_dict,
                    "$setOnInsert": {"created_at": datetime.now()}
                },
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error en Mongo: {e}")
            return False

db_manager = MongoDB()