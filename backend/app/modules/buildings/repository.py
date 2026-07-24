from motor.motor_asyncio import AsyncIOMotorDatabase

from app.modules.buildings.models import BuildingModel
from app.shared.repository import BaseRepository
from app.shared.object_id import to_object_id


class BuildingRepository(BaseRepository):

    COLLECTION_NAME = "buildings"

    def __init__(self, db: AsyncIOMotorDatabase):
        super().__init__(db[self.COLLECTION_NAME])

    async def create_building(
        self,
        building: BuildingModel,
    ) -> str:
        return await self.create(
            building.model_dump(exclude={"id"})
        )

    async def get_by_id(
        self,
        building_id: str,
        world_id: str,
    ) -> dict | None:
        return await self.find_one(
            {
                "_id": to_object_id(building_id),
                "world_id": world_id,
            }
        )

    async def get_by_type(
        self,
        world_id: str,
        building_type: str,
    ) -> dict | None:
        return await self.find_one(
            {
                "world_id": world_id,
                "type": building_type,
            }
        )

    async def list_by_world(
        self,
        world_id: str,
    ) -> list[dict]:
        return await self.find(
            filter_query={
                "world_id": world_id,
            }
        )

    async def update_building(
        self,
        building_id: str,
        world_id: str,
        update_data: dict,
    ):
        return await self.update(
            filter_query={
                "_id": to_object_id(building_id),
                "world_id": world_id,
            },
            update_data=update_data,
        )

    async def delete_building(
        self,
        building_id: str,
        world_id: str,
    ):
        return await self.delete(
            {
                "_id": to_object_id(building_id),
                "world_id": world_id,
            }
        )