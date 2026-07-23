# model represents how we store data internally.
from datetime import datetime, UTC
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from app.shared.utils import utc_now
from app.shared.enums import WorldRace


# provide a balanced early game
# player immediately start constructing buildings without a long idle period
class WorldModel(BaseModel):
    id: Optional[str] = None
    owner_id: str
    name: str = Field(min_length=3, max_length=50)
    race: WorldRace
    gold: int = 500
    wood: int = 300
    stone: int = 250
    food: int = 400
    population: int = 25
    created_at: datetime = Field(default_factory=lambda: utc_now())
    updated_at: datetime = Field(default_factory=lambda: utc_now())