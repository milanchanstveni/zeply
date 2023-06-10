"""Exceptions for HTTP errors."""

from fastapi import (
    HTTPException,
    status
)


class BaseHTTPException(HTTPException):
    """Base class for HTTP exceptions."""

    def __init__(self, *args, status_code: int, detail: str = None, **kwargs):
        """Initialize class."""
        super().__init__(
            *args, status_code=status_code, detail=detail, **kwargs
        )


class CoinNotImplemented(BaseHTTPException):
    """Coin not implemented exception."""

    def __init__(self, *args, **kwargs):
        """Initialize class."""
        super().__init__(
            *args,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coin not implemented.",
            **kwargs
        )


class InvalidCoin(BaseHTTPException):
    """Invalid coin exception."""

    def __init__(self, *args, **kwargs):
        """Initialize class."""
        super().__init__(
            *args,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid coin.",
            **kwargs
        )


class ObjectNotFound(BaseHTTPException):
    """Object not found exception."""

    def __init__(self, *args, **kwargs):
        """Initialize class."""
        super().__init__(
            *args,
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Object not found.",
            **kwargs
        )


class UnknownError(BaseHTTPException):
    """Unknown error exception."""

    def __init__(self, *args, **kwargs):
        """Initialize class."""
        super().__init__(
            *args,
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown error: {args}/{kwargs}",
            **kwargs
        )
