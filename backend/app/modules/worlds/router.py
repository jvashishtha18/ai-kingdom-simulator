from fastapi import Depends, APIRouter

from app.core.dependencies import get_world_service
from app.modules.worlds.service import WorldService
from app.modules.worlds.schemas import CreateWorldRequest

router = APIRouter(prefix="/worlds", tags=["Worlds"])
@router.post("")
async def create_world(
    request: CreateWorldRequest,
    service: WorldService = Depends(get_world_service),
):
    ...