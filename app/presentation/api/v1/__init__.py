from fastapi import APIRouter
from .users import router as users_router


routers = [users_router]

v1_router = APIRouter(prefix="/v1")
for router in routers:
    v1_router.include_router(router)
