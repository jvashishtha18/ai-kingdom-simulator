from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.shared.enums import Role
from app.core.config import settings
# Why separate Schemas and Models?
# Our internal database model contains:
# password_hash
# created_at
# updated_at
# We should never expose those fields to the frontend.
# Instead, UserResponse contains only the information we want to return.


class RegisterRequest(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50,
    )
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=100,
    )
    role: Role


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: str
    name: str
    email: EmailStr
    is_active: bool
    role: Role

class AuthenticatedUser(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: Role

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    user: AuthenticatedUser