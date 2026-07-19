from pydantic import BaseModel, EmailStr, Field, ConfigDict
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