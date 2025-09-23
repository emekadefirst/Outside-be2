from fastapi import HTTPException, status
from tortoise import Model
from typing import Type


class ErrorMessage:
    def __init__(self, model: Type[Model]):
        self.model = model.__name__

    def not_found(self):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{self.model} not found",
        )

    def already_exists(self):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{self.model} already exists",
        )

    def bad_request(self, message: str = "Bad request"):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{self.model}: {message}",
        )

    def unauthorized(self, message: str = "Unauthorized"):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{self.model}: {message}",
        )

    def forbidden(self, message: str = "Forbidden"):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{self.model}: {message}",
        )

    def conflict(self, message: str = "Conflict"):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{self.model}: {message}",
        )

    def unprocessable(self, message: str = "Unprocessable Entity"):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{self.model}: {message}",
        )

    def internal_error(self, message: str = "Internal Server Error"):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{self.model}: {message}",
        )

    def service_unavailable(self, message: str = "Service Unavailable"):
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"{self.model}: {message}",
        )
