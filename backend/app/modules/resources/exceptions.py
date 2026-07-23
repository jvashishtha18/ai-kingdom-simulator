from http import HTTPStatus

from app.core.exceptions import AppException


class ResourceNotFoundException(AppException):
    def __init__(
        self,
        message: str = "Resource record not found.",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            status_code=HTTPStatus.NOT_FOUND,
            details=details,
        )


class InvalidResourceAmountException(AppException):
    def __init__(
        self,
        message: str = "Resource amount must be greater than zero.",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            status_code=HTTPStatus.BAD_REQUEST,
            details=details,
        )


class InsufficientResourcesException(AppException):
    def __init__(
        self,
        message: str = "Insufficient resources.",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            status_code=HTTPStatus.BAD_REQUEST,
            details=details,
        )