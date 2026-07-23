from fastapi import APIRouter, Depends, Response, status

from app.core.dependencies import (
    get_current_user,
    get_world_service,
)
from app.modules.auth.schemas import UserResponse
from app.modules.worlds.schemas import (
    CreateWorldRequest,
    UpdateWorldRequest,
    WorldResponse,
    WorldSummaryResponse,
)
from app.modules.worlds.service import WorldService

router = APIRouter()

@router.post(
    "",
    response_model=WorldResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new world",
)
async def create_world(
    request: CreateWorldRequest,
    current_user: UserResponse = Depends(get_current_user),
    world_service: WorldService = Depends(get_world_service),
) -> WorldResponse:
    return await world_service.create_world(
        owner_id=current_user.id,
        request=request,
    )

@router.get(
    "",
    response_model=list[WorldSummaryResponse],
    summary="List my worlds",
)
async def list_worlds(
    current_user: UserResponse = Depends(get_current_user),
    world_service: WorldService = Depends(get_world_service),
) -> list[WorldSummaryResponse]:
    return await world_service.list_worlds(
        owner_id=current_user.id,
    )

@router.get(
    "/{world_id}",
    response_model=WorldResponse,
    summary="Get world",
)
async def get_world(
    world_id: str,
    current_user: UserResponse = Depends(get_current_user),
    world_service: WorldService = Depends(get_world_service),
) -> WorldResponse:
    return await world_service.get_world(
        owner_id=current_user.id,
        world_id=world_id,
    )

@router.put(
    "/{world_id}",
    response_model=WorldResponse,
    summary="Update world",
)
async def update_world(
    world_id: str,
    request: UpdateWorldRequest,
    current_user: UserResponse = Depends(get_current_user),
    world_service: WorldService = Depends(get_world_service),
) -> WorldResponse:
    return await world_service.update_world(
        owner_id=current_user.id,
        world_id=world_id,
        request=request,
    )

@router.delete(
    "/{world_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete world",
)
async def delete_world(
    world_id: str,
    current_user: UserResponse = Depends(get_current_user),
    world_service: WorldService = Depends(get_world_service),
) -> Response:
    await world_service.delete_world(
        owner_id=current_user.id,
        world_id=world_id,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )