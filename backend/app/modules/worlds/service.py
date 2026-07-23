from datetime import UTC, datetime

from app.core.exceptions import (
    WorldAlreadyExistsException,
    WorldNotFoundException,
)
from app.modules.worlds.models import WorldModel
from app.modules.worlds.repository import WorldRepository
from app.modules.worlds.schemas import (
    CreateWorldRequest,
    UpdateWorldRequest,
    WorldResponse,
    WorldSummaryResponse,
)


class WorldService:
    """
    Business logic for World operations.
    """
    def __init__(self, repository: WorldRepository):
        self.repository = repository

    async def create_world(
        self,
        owner_id: str,
        request: CreateWorldRequest,
    ) -> WorldResponse:

        exists = await self.repository.exists_by_name(
            owner_id=owner_id,
            name=request.name,
        )

        if exists:
            raise WorldAlreadyExistsException(
                details={
                    "world_name": request.name,
                }
            )

        world = WorldModel(
            owner_id=owner_id,
            name=request.name,
            race=request.race,
        )

        created_world = await self.repository.create_world(world)

        return WorldResponse(**created_world)

    async def get_world(
        self,
        world_id: str,
    ) -> WorldResponse:

        world = await self.repository.get_world(world_id)

        if world is None:
            raise WorldNotFoundException(
                details={
                    "world_id": world_id,
                }
            )

        return WorldResponse(**world)

    async def list_worlds(
        self,
        owner_id: str,
    ) -> list[WorldSummaryResponse]:

        worlds = await self.repository.list_worlds_by_owner(owner_id)

        return [
            WorldSummaryResponse(
                id=world["id"],
                name=world["name"],
                race=world["race"],
                population=world["population"],
            )
            for world in worlds
        ]

    async def update_world(
        self,
        world_id: str,
        request: UpdateWorldRequest,
    ) -> WorldResponse:

        world = await self.repository.get_world(world_id)

        if world is None:
            raise WorldNotFoundException(
                details={
                    "world_id": world_id,
                }
            )

        update_data = request.model_dump(exclude_none=True)

        update_data["updated_at"] = datetime.now(UTC)

        updated_world = await self.repository.update_world(
            world_id,
            update_data,
        )

        return WorldResponse(**updated_world)

    async def delete_world(
        self,
        world_id: str,
    ) -> None:

        world = await self.repository.get_world(world_id)

        if world is None:
            raise WorldNotFoundException(
                details={
                    "world_id": world_id,
                }
            )

        await self.repository.delete_world(world_id)