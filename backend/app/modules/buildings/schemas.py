from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.modules.buildings.enums import (
    BuildingStatus,
    BuildingType,
)


class CreateBuildingRequest(BaseModel):
    type: BuildingType

class BuildingResponse(BaseModel):
    id: str
    world_id: str
    type: BuildingType
    level: int
    status: BuildingStatus
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
# this is useful if you later return models instead of dictionaries.
    model_config = ConfigDict(
        from_attributes=True
    )

class BuildingSummaryResponse(BaseModel):
    id: str
    type: BuildingType
    level: int
    status: BuildingStatus

    model_config = ConfigDict(
        from_attributes=True
    )
    
class BuildingCatalogResponse(BaseModel):
    type: BuildingType
    name: str
    description: str
    max_level: int
    build_time: int
    cost: dict[str, int]
    production: dict[str, int]

    model_config = ConfigDict(
        from_attributes=True
    )