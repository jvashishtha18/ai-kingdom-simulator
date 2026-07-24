from http import HTTPStatus

from app.core.exceptions import AppException


class BuildingNotFoundException(AppException):
    def __init__(
        self,
        message: str = "Building not found.",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            status_code=HTTPStatus.NOT_FOUND,
            details=details,
        )


class BuildingAlreadyExistsException(AppException):
    def __init__(
        self,
        message: str = "Building already exists.",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            status_code=HTTPStatus.CONFLICT,
            details=details,
        )


class BuildingMaxLevelException(AppException):
    def __init__(
        self,
        message: str = "Building has reached the maximum level.",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            status_code=HTTPStatus.BAD_REQUEST,
            details=details,
        )


class BuildingRequirementException(AppException):
    def __init__(
        self,
        message: str = "Building requirements are not satisfied.",
        details: dict | None = None,
    ):
        super().__init__(
            message=message,
            status_code=HTTPStatus.BAD_REQUEST,
            details=details,
        )