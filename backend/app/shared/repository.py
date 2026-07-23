from typing import Any
from motor.motor_asyncio import AsyncIOMotorCollection
from app.shared.object_id import to_object_id
from app.core.exceptions import NotFoundException
from pymongo import ReturnDocument
from backend.app.modules.auth.model import UserModel

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
    
    async def get_by_id(
    self,
    user_id: str,
    ) -> UserModel | None:
        document = await self.collection.find_one(
            {
                "_id": to_object_id(user_id)
            }
        )
        return self._to_model(document)

    async def delete(self,document_id: str,):
        result = await self.collection.delete_one({
          "_id": to_object_id(document_id)  
        })
        if result.deleted_count == 0:
            raise NotFoundException("Document not found")
        return True
    
    async def update(self,document_id: str,data: dict[str, Any])->dict[str, Any]:
         return await self.collection.find_one_and_update(
            {"_id": to_object_id(document_id)},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
    
    async def list(
        self,
        *,
        filter_query: dict[str, Any] | None = None,
        page: int = 1,
        page_size: int = 20,
        sort_field: str = "_id",
        sort_order: int = 1,
    ):
        filter_query = filter_query or {}

        cursor = (
            self.collection.find(filter_query)
            .sort(sort_field, sort_order)
            .skip((page - 1) * page_size)
            .limit(page_size)
        )

        return await cursor.to_list(length=page_size)

    async def count(
        self,
        filter_query: dict[str, Any] | None = None,
    ) -> int:
        return await self.collection.count_documents(
            filter_query or {}
        )
    

