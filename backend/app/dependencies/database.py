# Why dependency injection?
# Instead of: from app.db.database import database 
# inside every file,
# we'll later use: db: AsyncIOMotorDatabase = Depends(get_database)

# Benefits:

# easier testing
# loose coupling
# cleaner architecture

from motor.motor_asyncio import AsyncIOMotorDatabase
from app.db.database import database

def get_database() -> AsyncIOMotorDatabase :
    if database is none:
        raise RuntimeError("Database has not been initialized.")
    
    return database