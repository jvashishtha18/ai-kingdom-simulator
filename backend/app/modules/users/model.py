from datetime import UTC, datetime
from typing import Any


def create_user_document(
    *,
    name: str,
    email: str,
    password_hash: str,
) -> dict[str, Any]:
    """
    Factory function to create a MongoDB user document.
    """

    now = datetime.now(UTC)

    return {
        "name": name,
        "email": email.lower(),
        "password_hash": password_hash,
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    }