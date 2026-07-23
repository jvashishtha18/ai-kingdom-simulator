from fastapi import APIRouter, Depends, status
from typing import Annotated

from app.core.dependencies import get_auth_service, get_current_user
from app.modules.auth.schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserResponse,
)
from app.modules.auth.service import AuthService

AuthServiceDep = Annotated[
    AuthService,
    Depends(get_auth_service),
]

router = APIRouter()

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    request: RegisterRequest,
    auth_service: AuthServiceDep,
):
    return await auth_service.register(request)

@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login user",
)
async def login(
    request: LoginRequest,
    auth_service: AuthServiceDep,
):
    return await auth_service.login(request)

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
)
async def get_current_user_profile(
   current_user=Depends(get_current_user),
):
    return await current_user