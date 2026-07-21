from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import (
    close_mongo_connection,
    connect_to_mongo,
)
from app.core.logger import configure_logging, logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Starting AI Kingdom Simulator API...")

    await connect_to_mongo()
    logger.info("MongoDB connected.")

    yield

    await close_mongo_connection()
    logger.info("MongoDB connection closed.")