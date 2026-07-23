from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr
from app.modules.auth.schemas import UserResponse


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
    def to_response(self) -> UserResponse:
        return UserResponse(
            id=self.id,
            name=self.name,
            email=self.email,
            is_active=self.is_active,
        )