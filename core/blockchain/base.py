import random
import string
from abc import (
    ABC,
    abstractmethod,
    abstractclassmethod,
    abstractproperty
)
from typing import (
    Any,
    Optional,
    List
)
from pydantic import (
    BaseModel,
    Field
)

import coinaddrvalidator


def generate_seed(num_of_words: int = 12) -> str:
    words = []
    letters = string.ascii_lowercase+string.digits+string.ascii_uppercase
    for _ in range(num_of_words):
        words.append(''.join(random.choice(letters) for i in range(5)))
    
    return ' '.join(words)


class Model(BaseModel):
    """Base model class."""

    class Config:
        orm_mode = True


class Address(Model):
    id: Optional[int]
    address: str
    coin_acronym: str
    coin_name: str
    network: str
    is_active: bool
    seed: str


class Key(Model):
    id: Optional[int]
    private_key: str
    public_key: Optional[str]
    addresses: Optional[List[Address]] = Field(..., nullable=True)


class Account(Model):
    id: Optional[int]
    coin: str
    # _ : KW_ONLY
    key: Key


class Base(ABC):
    """Abstact class for all cryptocurrencies wrappers."""

    @abstractclassmethod
    def account(cls, seed: str = "") -> Account:
        ...

    @abstractclassmethod
    def account_from_key(cls, key: str) -> Account:
        ...


class Coin(Base):
    """Base class for all cryptocurrencies wrappers."""

    @classmethod
    def is_valid_address(cls, coin: str, address: str) -> bool:
        """Validate if a given address is valid."""
        return coinaddrvalidator.validate(coin, address).valid
    
    @classmethod
    def is_valid_seed(cls, seed: str) -> bool:
        """Validate if a given seed is valid."""
        return len(seed.split()) > 11
    
    @abstractclassmethod
    def is_valid_private_key(self, private_key: str) -> bool:
        """Validate if a given private key is valid."""
        ...

    @abstractclassmethod
    def account(cls, num_of_addresses: int = 1) -> Account:
        """Generate a new account."""
        ...
    
    @abstractclassmethod
    def account_from_key(cls, key: str) -> Account:
        """Generate a new account from a private key."""
        ...
    
