from datetime import datetime, timezone
from pydantic import BaseModel , EmailStr, Field, ConfigDict

class User(BaseModel):
    # Represents a user stored in MongoDB.

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
# Why alias="_id"?
# MongoDB stores _id
# Python code should use id
# Pydantic maps them automatically.
    id: str | None = Field(default=None, alias="_id")
    name: str
    email: EmailStr
# Why store password_hash?
# Never save a user's password directly.
# ❌ Bad:
# password = "mypassword123"
# If the database is compromised, every user's password is exposed.
# ✅ Good:
# password_hash = "$2b$12$P2..."
# The original password cannot be recovered from the hash.
    password_hash: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
