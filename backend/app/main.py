from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logger import logger, setup_logger
from app.core.database import (
    close_mongo_connection,
    connect_to_mongo,
)

# Why use lifespan?
# Older FastAPI versions used:
# @app.on_event("startup")
# Now the recommended approach is:
# Application Starts
# ↓
# Connect Mongo
# ↓
# Run APIs
# ↓
# Shutdown
# ↓
# Close Mongo
# Everything related to startup and shutdown stays together.

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    logger.info("Starting application...")
    await connect_to_mongo()
    logger.info("MongoDB connected.")
    yield
    logger.info("Stopping application...")
    await close_mongo_connection()
    logger.info("MongoDB disconnected.")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.include_router(
    api_router,
    prefix=settings.API_PREFIX,
)

