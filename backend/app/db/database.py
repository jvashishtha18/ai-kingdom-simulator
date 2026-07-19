from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from app.core.config import settings

client: AsyncIOMotorClient | None = None
database: AsyncIOMotorDatabase | None = None


async def connect_to_mongo() -> None:
# Why globals here?
# There should be one MongoDB client for the application.
# Creating a new client for every request wastes resources.
    global client, database

    client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = client[settings.DATABASE_NAME]


async def close_mongo_connection() -> None:
    global client

    if client:
        client.close()


# Now, instead of accessing the database directly:
# db["users"]
# we'll consistently use:
# get_collection("users")
# This keeps our code cleaner and makes it easier to change the implementation later if needed.
def get_collection(name: str) -> AsyncIOMotorCollection:
    if database is None:
        raise RuntimeError("Database has not been initialized.")

    return database[name]