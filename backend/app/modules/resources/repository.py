from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.modules.resources.models import ResourceModel
from app.shared.repository import BaseRepository
from app.modules.resources.enums import ResourceType

class ResourceRepository(BaseRepository):

    COLLECTION_NAME = "resources"

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db[self.COLLECTION_NAME])

    async def create_resources(
        self,
        resource: ResourceModel,
    ) -> str:
        return await self.create(
            resource.model_dump(exclude={"id"})
        )
    
    async def get_by_world_id(
        self,
        world_id: str,
    ) -> dict[str, Any] | None:
        return await self.find_one(
            {
            "world_id": world_id,
            }
        )
    
    async def update_resource(
        self,
        world_id: str,
        resource_type: ResourceType,
        amount: int,
   ):
        return await self.collection.find_one_and_update(
            {
                "world_id": world_id,
            },
            {
                "$inc": {
                    f"resources.{resource_type.value}": amount
                }
            },
            return_document=True,
        )
        
    async def update_resources(
        self,
        world_id: str,
        resource_updates: dict[ResourceType, int],
    ):
        increments = {
            f"resources.{resource.value}": amount
            for resource, amount in resource_updates.items()
        }

        return await self.collection.find_one_and_update(
            {
                "world_id": world_id,
            },
            {
                "$inc": increments,
            },
            return_document=True,
        )

    async def get_by_world(
        self,
        world_id: str,
    ) -> list[dict]:
        
        return await self.find(
            filter_query={
                "world_id": world_id,
            }
        )
                
