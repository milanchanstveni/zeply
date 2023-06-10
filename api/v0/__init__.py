from fastapi import APIRouter

from api.v0.routes.address import AddressRouter


API0 = APIRouter()

API0.include_router(AddressRouter)
