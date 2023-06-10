from typing import Optional
from pydantic import BaseModel, Field


class AddressPayload(BaseModel):
    coin: str = Field(..., example="BTC")

