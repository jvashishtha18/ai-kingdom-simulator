# only perform CRUD operations.
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.shared.repository import BaseRepository
from app.modules.worlds.models import WorldModel
from app.shared.object_id import to_object_id



class WorldRepository(BaseRepository):
    COLLECTION_NAME = "worlds"

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db[self.COLLECTION_NAME])

    async def create_world(self, world: WorldModel)-> str:
        return await self.create(world.model_dump())

    async def get_by_id(
    self,
    world_id: str,
    owner_id: str,
) -> dict | None:
        return await self.collection.find_one(
    {
        "_id": to_object_id(world_id),
        "owner_id": owner_id,
    }
)

    async def list_worlds_by_owner(
        self,
        owner_id: str,
) -> List[dict]:
        return await self.find(
            {
                "owner_id": owner_id,
            }
        )

    async def exists_by_name(
        self,
        owner_id: str,
        name: str,
    ) -> bool:

        world = await self.find_one(
            {
                "owner_id": owner_id,
                "name": name,
            }
        )

        return world is not None
    
    async def update_world(
    self,
    world_id: str,
    owner_id: str,
    update_data: dict,
) -> dict | None:
        
        return await self.update(
            filter_query={
                "_id": to_object_id(world_id),
                "owner_id": owner_id,
            },
            update_data=update_data,
        )

    async def delete_world(
    self,
    world_id: str,
    owner_id: str,
):
        return await self.delete(
            {
                "_id": to_object_id(world_id),
                "owner_id": owner_id,
            }
        )