from pydantic import Field, BaseModel
from datetime import datetime
from app.modules.resources.constants import INITIAL_RESOURCES
from app.shared.utils import utc_now
from app.modules.resources.enums import ResourceType

class ResourceModel(BaseModel):
    world_id: str

    resources: dict[ResourceType, int] = Field(
        default_factory=lambda: INITIAL_RESOURCES.copy()
    )

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)