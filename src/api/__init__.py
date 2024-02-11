from fastapi import APIRouter

from .v1 import v1_router

root_router = APIRouter()

@root_router.get("/")
async def index():
    return {"msg": "hello world"}

root_router.include_router(v1_router)
