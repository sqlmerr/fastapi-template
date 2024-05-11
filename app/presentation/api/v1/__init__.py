from fastapi import APIRouter

from .auth import router as auth_router
from .posts import router as posts_router
from .roles import router as roles_router

routers = [auth_router, posts_router, roles_router]

v1_router = APIRouter(prefix="/v1")
for router in routers:
    v1_router.include_router(router)
