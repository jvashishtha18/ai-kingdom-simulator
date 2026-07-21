from typing import Any
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from app.core.exceptions import NotFoundException

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
        document = await self.collection.find_one(
            {
                "_id": ObjectId(document_id)
            }
        )
        if not document:
            raise NotFoundException("Document not found")
        document['_id']=str(document["_id"])
        return document
    
    async def delete(self,document_id: str,):
        result = await self.collection.delete_one({
          "_id": ObjectId(document_id)  
        })
        if result.deleted_count == 0:
            raise NotFoundException("Document not found")
        return True
    
    async def update(self,document_id: str,data: dict[str, Any])->dict[str, Any]:
        result = await self.collection.update_one(
            {
                "_id": ObjectId(document_id)
            },
            {
                "$set": data
            },
        )
        if result.matched_count == 0:
            raise NotFoundException("Document not found")
        
        return await self.get_by_id(document_id)
    
    async def list(
        self,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        skip: int = 0,
    )->list[dict[str, Any]]:

        filters = filters or {}

        documents = await self.collection.find(filters).skip(skip).limit(limit).to_list(limit)
        for document in documents:
            document["_id"] = str(document["_id"])
        return documents
    

