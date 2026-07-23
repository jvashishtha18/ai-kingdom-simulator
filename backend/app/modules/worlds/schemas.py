# schemas represent what the client sends and receives
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.shared.enums import WorldRace


class CreateWorldRequest(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=50,
        description="Kingdom name",
    )

    race: WorldRace


class UpdateWorldRequest(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
    )


class WorldResponse(BaseModel):
    id: str
    owner_id: str
    name: str
    race: WorldRace
    gold: int
    wood: int
    stone: int
    food: int
    population: int
    created_at: datetime
    updated_at: datetime


class WorldSummaryResponse(BaseModel):
    id: str
    name: str
    race: WorldRace
    population: int