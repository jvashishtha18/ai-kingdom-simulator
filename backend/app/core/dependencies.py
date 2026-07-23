from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.modules.auth.service import AuthService
from backend.app.modules.auth.repository import UserRepository


def get_db() -> AsyncIOMotorDatabase:
    """
    Return the MongoDB database instance.
    """
    return get_database()


def get_user_repository(
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> UserRepository:
    """
    Create a UserRepository instance.
    """
    return UserRepository(db)


def get_auth_service(
    repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    """
    Create an AuthService instance.
    """
    return AuthService(repository)