# Instead of writing
# raise HTTPException(
#     status_code=404,
#     detail="User not found"
# )
# throughout the codebase, we'll simply use:
# raise NotFoundException("User not found")
# Later, a single exception handler will convert these into HTTP responses.
from typing import Any

ExceptionDetails = dict[str, Any]
class AppException(Exception):

    def __init__(
            self,
            message: str,
            error_code: str,
            status_code: int,
            details: ExceptionDetails | None = None, 
            ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code 
        self.details = details
        super().__init__(message)

class BadRequestException(AppException):
    def __init__(self, 
                 message: str = "Bad request",
                 error_code='BADREQUEST',
                 details: ExceptionDetails | None = None, ):
        super().__init__(
                message=message,
                error_code=error_code,
                status_code=400,
                details=details,
              )

class UnauthorizedException(AppException):

    def __init__(self, 
                 message="Unauthorized",
                 error_code='UNAUTHORIZED',
                 details: ExceptionDetails | None = None, 
                 ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=401,
            details=details,
            )

class ForbiddenException(AppException):
    def __init__(self, 
                 message: str = "Forbidden",
                 error_code = 'FORBIDDEN',
                 details: ExceptionDetails | None = None,):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=403,
            details=details,
            )

class NotFoundException(AppException):

    def __init__(
                 self, 
                 error_code='NOTFOUND',
                 message="Resource not found",
                 details: ExceptionDetails | None = None,
                 ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=404,
            details=details,
            )

class ConflictException(AppException):

    def __init__(
             self, 
             message="Resource already exists",
             error_code: str = "CONFLICT",
             details: ExceptionDetails | None = None,
             ):
        super().__init__(
            message=message,
            error_code=error_code,
            status_code=409,
            details=details,
                         )

class WorldNotFoundException(NotFoundException):
    def __init__( 
            self,
            details: ExceptionDetails | None = None,
                 ):
        super().__init__(
            message="World not found.",
            error_code="WORLD_NOT_FOUND",
            status_code=409,
            details=details,
        )

class WorldAlreadyExistsException(ConflictException):
    def __init__(self,details):
        super().__init__(
            message="World with this name already exists.",
            error_code="WORLD_ALREADY_EXISTS",
            status_code=409,
            details=details,
        )


