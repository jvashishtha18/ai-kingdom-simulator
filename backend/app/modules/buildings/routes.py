from fastapi import APIRouter, Depends, Response, status

from app.core.dependencies import (
    get_building_service,
    get_current_user,
)
from app.modules.auth.schemas import UserResponse
from app.modules.buildings.enums import BuildingType
from app.modules.buildings.schemas import (
    BuildingCatalogResponse,
    BuildingResponse,
    BuildingSummaryResponse,
    CreateBuildingRequest,
)
from app.modules.buildings.service import BuildingService

router = APIRouter()

@router.post(
    "/worlds/{world_id}/buildings",
    response_model=BuildingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Construct a building",
)
async def create_building(
    world_id: str,
    request: CreateBuildingRequest,
    current_user: UserResponse = Depends(get_current_user),
    building_service: BuildingService = Depends(get_building_service),
):
    return await building_service.build(
        world_id=world_id,
        building_type=request.type,
    )

@router.get(
    "/worlds/{world_id}/buildings",
    response_model=list[BuildingSummaryResponse],
    summary="List buildings",
)
async def list_buildings(
    world_id: str,
    current_user: UserResponse = Depends(get_current_user),
    building_service: BuildingService = Depends(get_building_service),
):
    return await building_service.list_buildings(
        world_id=world_id,
    )

@router.get(
    "/worlds/{world_id}/buildings/{building_id}",
    response_model=BuildingResponse,
    summary="Get building",
)
async def get_building(
    world_id: str,
    building_id: str,
    current_user: UserResponse = Depends(get_current_user),
    building_service: BuildingService = Depends(get_building_service),
):
    return await building_service.get_building(
        world_id=world_id,
        building_id=building_id,
    )

@router.put(
    "/worlds/{world_id}/buildings/{building_id}/upgrade",
    response_model=BuildingResponse,
    summary="Upgrade building",
)
async def upgrade_building(
    world_id: str,
    building_id: str,
    current_user: UserResponse = Depends(get_current_user),
    building_service: BuildingService = Depends(get_building_service),
):
    return await building_service.upgrade(
        world_id=world_id,
        building_id=building_id,
    )

@router.get(
    "/buildings/catalog",
    response_model=list[BuildingCatalogResponse],
    summary="Building catalog",
)
async def get_catalog(
    building_service: BuildingService = Depends(get_building_service),
):
    return await building_service.get_catalog()