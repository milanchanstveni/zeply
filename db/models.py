import datetime
from typing import (
    List,
    Any,
)

from tortoise.contrib.pydantic.base import (
    PydanticModel,
    PydanticListModel,
)
from tortoise.models import Model
from tortoise import (
    fields,
    Tortoise,
)
from tortoise.contrib.pydantic import (
    pydantic_model_creator,
    pydantic_queryset_creator
)


class Base:

    class Config:
        abstract = True
        orm_mode = True
    
    @classmethod
    def _init_models(cls) -> None:
        Tortoise.init_models(["db.models"], "models")

    def __init__(self) -> None:
        self._init_models()
        pass

    @classmethod
    @property
    def model(cls) -> PydanticModel:
        cls._init_models()
        obj = pydantic_model_creator(cls, name=f"{cls.__name__}Model")
        return obj
    
    @classmethod
    @property
    def model_list(cls) -> PydanticListModel:
        cls._init_models()
        obj = pydantic_queryset_creator(cls, name=f"{cls.__name__}ListModel")
        return obj


class Address(Model, Base):
    address = fields.CharField(max_length=255, unique=True)
    coin_acronym = fields.CharField(max_length=5)
    coin_name = fields.CharField(max_length=100)
    network = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    seed = fields.CharField(max_length=255, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"Address[{self.coin_acronym}]: {self.address}"


class Key(Model, Base):
    private_key = fields.CharField(max_length=255, unique=True)
    public_key = fields.CharField(max_length=255)
    addresses = fields.ManyToManyField(
        model_name="models.Address", related_name="keys", through="key_address"
    )

    def __str__(self):
        return f"Key[{self.public_key}] addresses: {self.addresses}"


class Account(Model, Base):
    coin = fields.CharField(max_length=5)
    key = fields.ForeignKeyField(
        model_name="models.Key", related_name="accounts", on_delete=fields.CASCADE
    )

    def __str__(self):
        return f"Account[{self.coin}]: {self.id}"

