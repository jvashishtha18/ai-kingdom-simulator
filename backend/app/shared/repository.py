from typing import Any
from motor.motor_asyncio import AsyncIOMotorCollection
from app.shared.object_id import to_object_id
from app.core.exceptions import NotFoundException
from pymongo import ReturnDocument

# we centralize those operations in one place.
# inherits all CRUD methods automatically.
class BaseRepository:

    def __init__(
        self,
        collection: AsyncIOMotorCollection,
    ):
        self.collection = collection
    
    async def create(self,data: dict)-> str:
        result = await self.collection.insert_one(data)
        return str(result.inserted_id)
    
    async def get_by_id(
    self,
    document_id: str,
    ) -> dict[str, Any] | None:
        return await self.collection.find_one(
            {
                "_id": to_object_id(document_id)
            }
        )
         

    async def delete(self,filter_query: dict[str, Any],) -> bool:
        result = await self.collection.delete_one(filter_query)

        if result.deleted_count == 0:
            raise NotFoundException("Document not found")
        return True
    
    async def update(self, filter_query: dict[str, Any], update_data: dict[str, Any],)-> dict[str, Any] | None:
        return await self.collection.find_one_and_update(
            filter_query,
            {"$set": update_data},
            return_document=ReturnDocument.AFTER,
        )
    
    async def find(
        self,
        *,
        filter_query: dict[str, Any] | None = None,
        page: int = 1,
        page_size: int = 20,
        sort_field: str = "_id",
        sort_order: int = 1,
    )-> list[dict[str, Any]]:
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

    async def find_one(
    self,
    filter_query: dict[str, Any],
) -> dict[str, Any] | None:
     return await self.collection.find_one(filter_query)
    

