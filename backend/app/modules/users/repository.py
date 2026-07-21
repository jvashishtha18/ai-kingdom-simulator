from motor.motor_asyncio import AsyncIOMotorDatabase
from app.shared.repository import BaseRepository


class UserRepository(BaseRepository):

    COLLECTION_NAME = "users"

    def __init__(self,database: AsyncIOMotorDatabase):
        super().__init__(
            database[self.COLLECTION_NAME]
        )

    async def find_by_email(
        self,
        email: str,
    ):
        user = await self.collection.find_one(
            {
                "email": email.lower()
            }
        )
        if user:
            user["_id"]= str(user["_id"])
        return user
    
    async def email_exists(self, email: str) -> bool:
        return (
            await self.collection.count_documents(
                {"email": email.lower()},
                limit=1,
            )
        ) > 0