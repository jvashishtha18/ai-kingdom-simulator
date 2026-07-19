from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

# every API returns the same shape.
# {
#   "success": true,
#   "message": "World created successfully.",
#   "data": {
#       ...
#   }
# }
class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None