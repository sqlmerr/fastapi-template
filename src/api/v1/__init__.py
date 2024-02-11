from fastapi import APIRouter
from . import users


v1_router = APIRouter(prefix="/v1")

v1_router.include_router(users.router)