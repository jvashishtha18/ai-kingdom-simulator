from app.core.database import get_collection
from backend.app.shared.repository import BaseRepository


class UserRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            get_collection("users")
        )

    async def find_by_email(
        self,
        email: str,
    ):
        user = await self.collection.find_one(
            {
                "email": email
            }
        )
        if user:
            user["_id"]= str(user["_id"])
        return user