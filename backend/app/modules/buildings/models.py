from pydantic import BaseModel
from datetime import datetime
from app.modules.buildings.enums import  (
    BuildingType, 
    BuildingStatus,
    )


class BuildingModel(BaseModel):
    id: str | None = None
    world_id: str
    type: BuildingType
    level: int = 1
    status: BuildingStatus
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime