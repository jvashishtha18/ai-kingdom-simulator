from datetime import datetime, timezone
from pydantic import BaseModel , EmailStr, Field

class User(BaseModel):
        id: str | None = None
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
        created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
        updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))
