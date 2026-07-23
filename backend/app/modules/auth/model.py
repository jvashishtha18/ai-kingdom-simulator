from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserModel(BaseModel):
    """
    Internal user domain model.
    Used inside the backend only.
    """

    id: str | None = None
    name: str
    email: EmailStr
    password_hash: str
    is_active: bool = True

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
    )