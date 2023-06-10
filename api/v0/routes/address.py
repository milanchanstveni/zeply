from fastapi import APIRouter
from api.v0.handlers.address import (
    generate_address,
    list_addresses,
    fetch_address
)

AddressRouter = APIRouter()


AddressRouter.add_api_route(
    path="/addresses",
    endpoint=generate_address,
    methods=["POST"],
    summary="Generate a new address",
    description="Generate a new address for a given coin",
)


AddressRouter.add_api_route(
    path="/addresses",
    endpoint=list_addresses,
    methods=["GET"],
    summary="List all addresses",
    description="List all addresses",
)

AddressRouter.add_api_route(
    path="/addresses/{id}",
    endpoint=fetch_address,
    methods=["GET"],
    summary="Fetch an address",
    description="Fetch an address",
)

