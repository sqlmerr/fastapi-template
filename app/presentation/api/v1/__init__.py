from fastapi import APIRouter
from .auth import router as auth_router


routers = [auth_router]

v1_router = APIRouter(prefix="/v1")
for router in routers:
    v1_router.include_router(router)
