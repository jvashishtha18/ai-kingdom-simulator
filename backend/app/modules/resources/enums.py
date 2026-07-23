from enum import Enum


class ResourceType(str, Enum):
    WOOD = "wood"
    FOOD = "food"
    STONE = "stone"
    IRON = "iron"
    GOLD = "gold"