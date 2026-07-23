from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.modules.auth.router import router as auth_router
from app.modules.worlds.router import router as worlds_router


api_router = APIRouter()

# Health
api_router.include_router(
    health_router,
    tags=["Health"],
)

# Authentication
api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)

# Worlds
api_router.include_router(
    worlds_router,
    prefix="/worlds",
    tags=["Worlds"],
)