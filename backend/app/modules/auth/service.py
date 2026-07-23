from datetime import UTC, datetime

from app.core.exceptions import (
    ConflictException,
    NotFoundException,
    UnauthorizedException,
)
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from backend.app.modules.auth.repository import UserRepository
from backend.app.modules.auth.models import UserModel
from app.modules.auth.schemas import (
    LoginRequest,
    RegisterRequest,
    UserResponse,
    TokenResponse
)
from app.shared.utils import utc_now

class AuthService:
    def __init__(self,user_repository:UserRepository):
        self.user_repository = user_repository
    async def register(self,request:RegisterRequest)->UserResponse:
        existing_user = await self.user_repository.email_exists(request.email)

        if existing_user:
            raise ConflictException("Email already registered.")
        
        user = UserModel(
            name=request.name,
            email=request.email,
            password_hash=hash_password(
                request.password
            ),
            is_active=True,
            created_at=utc_now(),
            updated_at=utc_now(),
        )

        user_id = await self.user_repository.create(user.model_dump(exclude={"id"}))

        return user.to_response()
    
    async def login(self,request:LoginRequest)->TokenResponse:
        user = await self.user_repository.find_by_email(request.email)
        if not user:
            raise UnauthorizedException(
                "Invalid email or password."
            )
        if not verify_password(request.password):
            raise UnauthorizedException(
                "Invalid email or password."
            )
        token = await create_access_token(str(user["_id"]))
        return TokenResponse(
            access_token = token
        )
    
    async def get_current_user(self,user_id:str)->UserResponse:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
             raise NotFoundException(
                "User not found."
            )
        return user.to_response()
    
    # Why create a Service layer instead of putting everything inside the Router?
    # The Service layer contains business logic independent of HTTP. Routers handle 
    # request/response concerns, repositories handle persistence, and services coordinate 
    # application behavior. This separation improves testability, reuse, and maintainability.
        