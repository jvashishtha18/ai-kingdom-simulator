from pydantic import BaseModel, EmailStr
# Why separate Schemas and Models?
# Our internal database model contains:
# password_hash
# created_at
# updated_at
# We should never expose those fields to the frontend.
# Instead, UserResponse contains only the information we want to return.

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr