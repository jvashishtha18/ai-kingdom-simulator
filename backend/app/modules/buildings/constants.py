from app.modules.buildings.building_definition import BuildingDefinition
from app.modules.buildings.enums import BuildingType
from app.modules.resources.enums import ResourceType

BUILDING_DEFINITIONS = {
    BuildingType.FARM: BuildingDefinition(
        name="Farm",
        description="Produces food.",
        build_time=60,
        max_level=20,
        base_cost={
            ResourceType.WOOD: 120,
            ResourceType.STONE: 40,
        },
        base_production={
            ResourceType.FOOD: 20,
        },
    ),

    BuildingType.LUMBER_MILL: BuildingDefinition(
        name="Lumber Mill",
        description="Produces wood.",
        build_time=90,
        max_level=20,
        base_cost={
            ResourceType.WOOD: 150,
            ResourceType.STONE: 80,
        },
        base_production={
            ResourceType.WOOD: 15,
        },
    ),
}