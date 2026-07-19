# Instead of writing

# raise HTTPException(
#     status_code=404,
#     detail="User not found"
# )

# throughout the codebase, we'll simply use:

# raise NotFoundException("User not found")

# Later, a single exception handler will convert these into HTTP responses.


class AppException(Exception):

    def __init__(
            self,
            message: str,
            status_code: int = 400, ):
        self.message = message
        self.status_code = status_code 

class NotFoundException(AppException):

    def __init__(self, message="Resource not found"):
        super().__init__(message, 404)

class ConflictException(AppException):

    def __init__(self, message="Conflict"):
        super().__init__(message, 409)

class UnauthorizedException(AppException):

    def __init__(self, message="Unauthorized"):
        super().__init__(message, 401)

