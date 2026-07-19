from app.core.database import get_collection
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):

    def __init__(self):
        super().__init__(
            get_collection("users")
        )

    async def find_by_email(
        self,
        email: str,
    ):
        return await self.collection.find_one(
            {
                "email": email
            }
        )