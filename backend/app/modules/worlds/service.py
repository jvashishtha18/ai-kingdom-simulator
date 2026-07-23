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
from app.shared.utils import utc_now
from app.modules.resources.service import ResourceService


class WorldService:
    """
    Business logic for World operations.
    """
    def __init__(
        self, 
        repository: WorldRepository,
        resource_service: ResourceService,
        ):
        self.repository = repository
        self.resource_service = resource_service
    
    async def _get_world_or_raise(
        self,
     world_id: str,
     owner_id: str,)-> dict:
        world = await self.repository.get_by_id(
            world_id=world_id,
            owner_id=owner_id,
        )

        if world is None:
            raise WorldNotFoundException(
                details={"world_id": world_id}
            )

        return world

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

        world_id = await self.repository.create_world(world)
        
        await self.resource_service.initialize_resources( world_id=world_id)
        
        created_world = await self.repository.get_by_id(
            world_id=world_id,
            owner_id=owner_id,
        )
        if created_world is None:
            raise WorldNotFoundException(
                details={"world_id": world_id}
            )
        return WorldResponse(**created_world)

    async def get_world(
        self, 
        owner_id: str, 
        world_id: str,) -> WorldResponse:

        world = await self._get_world_or_raise( world_id,owner_id,)

        return WorldResponse(**world)

    async def list_worlds(
        self,
        owner_id: str,
    ) -> list[WorldSummaryResponse]:

        worlds = await self.repository.list_worlds_by_owner(owner_id)

        return [
            WorldSummaryResponse(
                id=str(world["_id"]),
                name=world["name"],
                race=world["race"],
                population=world["population"],
            )
            for world in worlds
        ]

    async def update_world(
    self,
    owner_id: str,
    world_id: str,
    request: UpdateWorldRequest,
) -> WorldResponse:

        await self._get_world_or_raise(world_id,owner_id,)
        update_data = request.model_dump(exclude_none=True)

        update_data["updated_at"] = utc_now()

        updated_world = await self.repository.update_world(
            world_id=world_id,
            owner_id=owner_id,
            update_data=update_data,
        )
        if updated_world is None:
            raise WorldNotFoundException(
                details={"world_id": world_id}
        )
        return WorldResponse(**updated_world)

    async def delete_world(
        self,
        owner_id: str,
        world_id: str,
    ) -> None:

        await self._get_world_or_raise( world_id, owner_id,)

        await self.repository.delete_world(world_id=world_id,owner_id=owner_id,)