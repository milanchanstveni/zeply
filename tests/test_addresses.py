import pytest
from httpx import AsyncClient

from api.server import APP


@pytest.mark.anyio
async def test_create_address():
    async with AsyncClient(app=APP, base_url="http://test") as client:
        response = await client.post("/addresses", json={"coin": "BTC"})

    assert response.status_code == 200, response.text
    
    data = response.json()
    assert data.get("coin") == "BTC"
    assert data.get("id") is not None
    assert type(data.get("id")) == int and data.get("id") > 0
    assert data.get("key") is not None

    key = data["key"]
    assert type(key.get("id")) == int and key.get("id") > 0
    assert key.get("private_key") is not None
    assert len(key.get("private_key")) > 0
    assert key.get("public_key") is not None
    assert len(key.get("public_key")) > 0
    assert key.get("address") is not None

    address = key["address"]
    assert type(address.get("id")) == int and address.get("id") > 0
    assert address.get("address") is not None
    assert len(address.get("address")) > 0
    assert address.get("coin_acronym") == "BTC"
    assert address.get("coin_name") == "Bitcoin"
    assert address.get("network") == "mainnet"
    assert address.get("is_active") is True
    assert address.get("seed") is not None
    assert len(address.get("seed")) > 0
    

@pytest.mark.anyio
async def test_get_all_address(client: AsyncClient):
    async with AsyncClient(app=APP, base_url="http://test") as client:
        response = await client.get("/addresses")

    assert response.status_code == 200, response.text

    all_data = response.json()
    assert type(all_data) == list
    assert len(all_data) > 0

    data = all_data[0]
    assert data.get("coin") == "BTC"
    assert data.get("id") is not None
    assert type(data.get("id")) == int and data.get("id") > 0
    assert data.get("key") is not None

    key = data["key"]
    assert type(key.get("id")) == int and key.get("id") > 0
    assert key.get("private_key") is not None
    assert len(key.get("private_key")) > 0
    assert key.get("public_key") is not None
    assert len(key.get("public_key")) > 0
    assert key.get("address") is not None

    address = key["address"]
    assert type(address.get("id")) == int and address.get("id") > 0
    assert address.get("address") is not None
    assert len(address.get("address")) > 0
    assert address.get("coin_acronym") == "BTC"
    assert address.get("coin_name") == "Bitcoin"
    assert address.get("network") == "mainnet"
    assert address.get("is_active") is True
    assert address.get("seed") is not None
    assert len(address.get("seed")) > 0


@pytest.mark.anyio
async def test_get_address_by_id():
    async with AsyncClient(app=APP, base_url="http://test") as client:
        response = await client.get("/addresses/1")

    assert response.status_code == 200, response.text

    data = response.json()
    assert data.get("coin") == "BTC"
    assert data.get("id") is not None
    assert type(data.get("id")) == int and data.get("id") > 0
    assert data.get("key") is not None

    key = data["key"]
    assert type(key.get("id")) == int and key.get("id") > 0
    assert key.get("private_key") is not None
    assert len(key.get("private_key")) > 0
    assert key.get("public_key") is not None
    assert len(key.get("public_key")) > 0
    assert key.get("address") is not None

    address = key["address"]
    assert type(address.get("id")) == int and address.get("id") > 0
    assert address.get("address") is not None
    assert len(address.get("address")) > 0
    assert address.get("coin_acronym") == "BTC"
    assert address.get("coin_name") == "Bitcoin"
    assert address.get("network") == "mainnet"
    assert address.get("is_active") is True
    assert address.get("seed") is not None
    assert len(address.get("seed")) > 0
