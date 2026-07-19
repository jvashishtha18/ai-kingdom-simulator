# Every model will inherit from this.

# Instead of writing:
# created_at
# updated_at

# for every model, we inherit them automatically.

from datetime import datetime, timezone
from pydantic import BaseModel, Field


class TimestampModel(BaseModel):

    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))