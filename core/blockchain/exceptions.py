"""Exceptions for the crypto module."""


class BaseError(Exception):
    """Base for all database issues."""

    def __init__(self, message: str) -> None:
        """Initialize the exception."""
        Exception.__init__(self)

        self.message = message

    def __str__(self) -> str:
        return f"{self.message}"


class InvalidCoinError(BaseError):
    """Raised when the coin is invalid."""
    pass


class InvalidAddressError(BaseError):
    """Raised when the address is invalid."""
    pass


class InvalidPrivateKeyError(BaseError):
    """Raised when the private key is invalid."""
    pass


class InvalidPasswordError(BaseError):
    """Raised when the password is invalid."""
    pass


class InvalidSeedErrorBaseError(BaseError):
    """Raised when the seed is invalid."""
    pass


class InvalidKeyError(BaseError):
    """Raised when the key is invalid."""
    pass


class InvalidPublicKeyError(BaseError):
    """Raised when the public key is invalid."""
    pass


class InvalidMnemonicError(BaseError):
    """Raised when the mnemonic is invalid."""
    pass
