# only perform CRUD operations.
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.shared.repository import BaseRepository
from app.modules.worlds.models import WorldModel


class WorldRepository(BaseRepository):

    COLLECTION_NAME =  "worlds"

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db,self.COLLECTION_NAME)

    async def create_world(self, world: WorldModel):
        return await self.create(world.model_dump())

    async def get_world(self, world_id: str):
        return await self.get_by_id(world_id)

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
        data: dict,
    ):
        return await self.update(
            world_id,
            data,
        )

    async def delete_world(
        self,
        world_id: str,
    ):
        return await self.delete(world_id)