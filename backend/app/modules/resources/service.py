from app.modules.resources.enums import ResourceType
from app.modules.resources.exceptions import (
    InsufficientResourcesException,
    InvalidResourceAmountException,
    ResourceNotFoundException,
)
from app.modules.resources.models import ResourceModel
from app.modules.resources.repository import ResourceRepository


class ResourceService:
    """
    Handles all resource-related business logic.
    """

    def __init__(
        self,
        repository: ResourceRepository,
    ):
        self.repository = repository

    async def initialize_resources(
        self,
        world_id: str,
    ) -> None:
        """
        Creates the initial resource document for a world.
        """
        resource = ResourceModel(
            world_id=world_id,
        )

        await self.repository.create_resources(resource)

    async def get_resources(
        self,
        world_id: str,
    ) -> ResourceModel:
        """
        Returns all resources for a world.
        """
        resource = await self.repository.get_by_world_id(
            world_id=world_id,
        )

        if resource is None:
            raise ResourceNotFoundException(
                details={
                    "world_id": world_id,
                }
            )

        return ResourceModel(**resource)

    async def has_resource(
        self,
        world_id: str,
        resource_type: ResourceType,
        amount: int,
    ) -> bool:
        """
        Checks if a world has enough of a single resource.
        """
        resources = await self.get_resources(
            world_id=world_id,
        )

        return (
            resources.resources.get(resource_type, 0)
            >= amount
        )

    async def has_resources(
        self,
        world_id: str,
        required_resources: dict[ResourceType, int],
    ) -> bool:
        """
        Checks if a world has enough resources.
        """

        resources = await self.get_resources(
            world_id=world_id,
        )

        for resource_type, required_amount in required_resources.items():

            available = resources.resources.get(
                resource_type,
                0,
            )

            if available < required_amount:
                return False

        return True

    async def add_resource(
        self,
        world_id: str,
        resource_type: ResourceType,
        amount: int,
    ) -> None:
        """
        Adds a single resource.
        """

        if amount <= 0:
            raise InvalidResourceAmountException(
                details={
                    "resource": resource_type.value,
                    "amount": amount,
                }
            )

        await self.repository.update_resource(
            world_id=world_id,
            resource_type=resource_type,
            amount=amount,
        )

    async def consume_resource(
        self,
        world_id: str,
        resource_type: ResourceType,
        amount: int,
    ) -> None:
        """
        Consumes a single resource.
        """

        if amount <= 0:
            raise InvalidResourceAmountException(
                details={
                    "resource": resource_type.value,
                    "amount": amount,
                }
            )

        has_resource = await self.has_resource(
            world_id=world_id,
            resource_type=resource_type,
            amount=amount,
        )

        if not has_resource:

            resources = await self.get_resources(
                world_id=world_id,
            )

            available = resources.resources.get(
                resource_type,
                0,
            )

            raise InsufficientResourcesException(
                details={
                    "resource": resource_type.value,
                    "required": amount,
                    "available": available,
                }
            )

        await self.repository.update_resource(
            world_id=world_id,
            resource_type=resource_type,
            amount=-amount,
        )

    async def add_resources(
        self,
        world_id: str,
        resources_to_add: dict[ResourceType, int],
    ) -> None:
        """
        Adds multiple resources.
        """

        for resource_type, amount in resources_to_add.items():

            if amount <= 0:
                raise InvalidResourceAmountException(
                    details={
                        "resource": resource_type.value,
                        "amount": amount,
                    }
                )

        await self.repository.update_resources(
            world_id=world_id,
            resource_updates=resources_to_add,
        )

    async def consume_resources(
        self,
        world_id: str,
        required_resources: dict[ResourceType, int],
    ) -> None:
        """
        Consumes multiple resources.
        """

        resources = await self.get_resources(
            world_id=world_id,
        )

        for resource_type, amount in required_resources.items():

            available = resources.resources.get(
                resource_type,
                0,
            )

            if available < amount:
                raise InsufficientResourcesException(
                    details={
                        "resource": resource_type.value,
                        "required": amount,
                        "available": available,
                    }
                )

        updates = {
            resource_type: -amount
            for resource_type, amount
            in required_resources.items()
        }

        await self.repository.update_resources(
            world_id=world_id,
            resource_updates=updates,
        )