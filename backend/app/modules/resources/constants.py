from app.modules.resources.enums import ResourceType

resources: dict[ResourceType, int]

INITIAL_RESOURCES = {
    ResourceType.WOOD: 500,
    ResourceType.FOOD: 500,
    ResourceType.STONE: 300,
    ResourceType.IRON: 100,
    ResourceType.GOLD: 200,
}