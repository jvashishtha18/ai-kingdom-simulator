from app.modules.buildings.constants import BUILDING_DEFINITIONS
from app.modules.buildings.enums import BuildingType
from app.modules.buildings.exceptions import (
    BuildingAlreadyExistsException,
    BuildingMaxLevelException,
    BuildingNotFoundException,
)
from app.modules.buildings.models import BuildingModel
from app.modules.buildings.repository import BuildingRepository
from app.modules.buildings.schemas import (
    BuildingCatalogResponse,
    BuildingResponse,
    BuildingSummaryResponse,
)
from app.modules.resources.service import ResourceService
from app.shared.utils import utc_now



class BuildingService:

    def __init__(
        self,
        repository: BuildingRepository,
        resource_service: ResourceService,
    ):
        self.repository = repository
        self.resource_service = resource_service
    
    async def _get_building_or_raise(
        self,
        building_id: str,
        world_id: str,
    ):
        building = await self.repository.get_by_id(
            building_id=building_id,
            world_id=world_id,
        )

        if building is None:
            raise BuildingNotFoundException(
                details={
                    "building_id": building_id,
                }
            )

        return building


    async def build(
            self,
            world_id: str,
            building_type: BuildingType,
        ) -> BuildingResponse:

            exists = await self.repository.exists(
                {
                    "world_id": world_id,
                    "type": building_type.value,
                }
            )

            if exists:
                raise BuildingAlreadyExistsException(
                    details={
                        "building_type": building_type.value,
                    }
                )

            definition = BUILDING_DEFINITIONS[building_type]

            await self.resource_service.consume_resources(
                world_id=world_id,
                required_resources=definition.base_cost,
            )

            building = BuildingModel(
                world_id=world_id,
                type=building_type,
            )

            building_id = await self.repository.create_building(
                building
            )

            created_building = await self.repository.get_by_id(
                building_id=building_id,
                world_id=world_id,
            )

            if created_building is None:
                raise BuildingNotFoundException(
                    details={
                        "building_id": building_id,
                    }
                )

            return BuildingResponse(**created_building)

    async def get_building(
                self,
                world_id: str,
                building_id: str,
            ) -> BuildingResponse:

                building = await self._get_building_or_raise(
                    building_id=building_id,
                    world_id=world_id,
                )

                return BuildingResponse(**building)

    async def list_buildings(
                self,
                world_id: str,
            ) -> list[BuildingSummaryResponse]:

                buildings = await self.repository.list_by_world(
                    world_id=world_id,
                )

                return [
                    BuildingSummaryResponse(
                        id=str(building["_id"]),
                        type=building["type"],
                        level=building["level"],
                        status=building["status"],
                    )
                    for building in buildings
                ]

    async def get_catalog(self,) -> list[BuildingCatalogResponse]:
                        catalog = []
                        for building_type, definition in BUILDING_DEFINITIONS.items():
                            catalog.append(
                                BuildingCatalogResponse(
                                    type=building_type,
                                    name=definition.name,
                                    description=definition.description,
                                    max_level=definition.max_level,
                                    build_time=definition.build_time,
                                    cost={
                                        resource.value: amount
                                        for resource, amount in definition.base_cost.items()
                                    },
                                    production={
                                        resource.value: amount
                                        for resource, amount in definition.base_production.items()
                                    },
                                )
                            )

                        return catalog

    async def upgrade(
                  self,
                  world_id: str,
                  building_id: str,
                ) -> BuildingResponse:
                building = await self._get_building_or_raise(
                    building_id=building_id,
                    world_id=world_id,
                )

                building_type = BuildingType(building["type"])

                definition = BUILDING_DEFINITIONS[building_type]

                current_level = building["level"]

                if current_level >= definition.max_level:
                    raise BuildingMaxLevelException(
                        details={
                            "building_type": building["type"],
                            "max_level": definition.max_level,
                        }
                    )

                upgrade_cost = definition.get_upgrade_cost(
                    current_level
                )

                await self.resource_service.consume_resources(
                    world_id=world_id,
                    required_resources=upgrade_cost,
                )

                updated_building = await self.repository.update_building(
                    building_id=building_id,
                    world_id=world_id,
                    update_data={
                        "level": current_level + 1,
                        "updated_at": utc_now(),
                    },
                )

                if updated_building is None:
                    raise BuildingNotFoundException(
                        details={
                            "building_id": building_id,
                        }
                    )

                return BuildingResponse(**updated_building)