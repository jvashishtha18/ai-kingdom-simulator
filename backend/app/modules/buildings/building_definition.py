from typing import Callable

from pydantic import BaseModel

from app.modules.resources.enums import ResourceType


class BuildingDefinition(BaseModel):
    """
    Static configuration for a building type.
    """
    name: str
    description: str
    build_time: int
    max_level: int
    base_cost: dict[ResourceType, int]
    base_production: dict[ResourceType, int]
    prerequisites: dict[str, int] = {}
    cost_multiplier: float = 1.5
    production_multiplier: float = 1.2
    
    def get_upgrade_cost(
        self,
        level: int,
    ) -> dict[ResourceType, int]:

        multiplier = self.cost_multiplier ** (level - 1)
        return {
            resource: int(amount * multiplier)
            for resource, amount in self.base_cost.items()
        }

    def get_production(
        self,
        level: int,
    ) -> dict[ResourceType, int]:

        multiplier = self.production_multiplier ** (level - 1)
        return {
            resource: int(amount * multiplier)
            for resource, amount in self.base_production.items()
        }

    def get_build_cost(self,) -> dict[ResourceType, int]:
           return self.base_cost.copy()