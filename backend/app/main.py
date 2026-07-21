from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.handlers import register_exception_handlers

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

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)
register_exception_handlers(app)

app.include_router(
    api_router,
    prefix=settings.API_PREFIX,
)

