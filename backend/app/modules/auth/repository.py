from motor.motor_asyncio import AsyncIOMotorDatabase
from app.shared.repository import BaseRepository
from bson import ObjectId

from backend.app.modules.auth.models import UserModel


class UserRepository(BaseRepository):

    COLLECTION_NAME = "users"

    def __init__(self,database: AsyncIOMotorDatabase):
        super().__init__(
            database[self.COLLECTION_NAME]
        )
    
    def _to_model(self, document: dict | None) -> UserModel | None:
     if document is None:
        return None

     return UserModel(
        id=str(document["_id"]),
        name=document["name"],
        email=document["email"],
        password_hash=document["password_hash"],
        is_active=document["is_active"],
        created_at=document["created_at"],
        updated_at=document["updated_at"],
    )

    async def find_by_email(
        self,
        email: str,
    ) -> UserModel | None:

        document = await self.collection.find_one(
            {
                "email": email.lower()
            }
        )

        return self._to_model(document)

    async def email_exists(self, email: str) -> bool:
        return (
            await self.collection.count_documents(
                {"email": email.lower()},
                limit=1,
            )
        ) > 0