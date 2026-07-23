from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.security import OAuth2PasswordBearer

from app.core.database import get_database
from app.modules.auth.service import AuthService
from app.modules.auth.repository import UserRepository
from app.modules.worlds.repository import WorldRepository
from app.modules.worlds.service import WorldService
from app.core.security import decode_access_token


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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    payload = decode_access_token(token)

    return await auth_service.get_current_user(
        payload.user_id
    )

def get_world_repository(
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> WorldRepository:
    return WorldRepository(db)


def get_world_service(
    repository: WorldRepository = Depends(get_world_repository),
) -> WorldService:
    return WorldService(repository)