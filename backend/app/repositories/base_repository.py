from typing import Any
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

# we centralize those operations in one place.
# inherits all CRUD methods automatically.
class BaseRepository:

    def __init__(
        self,
        collection: AsyncIOMotorCollection,
    ):
        self.collection = collection
    
    async def create(self,data: dict):
        result = self.collection.insert_one(data)
        return str(result.inserted_id)
    
    async def get_by_id(self, document_id: str):
        return await self.collection.find_one(
            {
                "_id": ObjectId(document_id)
            }
        )
    
    async def delete(self,document_id: str,):
        return await self.collection.delete_one({
          "_id": ObjectId(document_id)  
        })
    
    async def update(self,document_id: str,data: dict,):
        await self.collection.update_one(
            {
                "_id": ObjectId(document_id)
            },
            {
                "$set": data
            },
        )

        return await self.get_by_id(document_id)
    
    async def list(
        self,
        filters: dict | None = None,
    ):

        filters = filters or {}

        return await self.collection.find(filters).to_list(100)
    

