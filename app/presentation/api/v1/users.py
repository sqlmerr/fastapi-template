from typing import Annotated

from fastapi import APIRouter, Depends
from app.presentation.interactor_factory import InteractorFactory
from app.application.authenticate import LoginDTO
from app.application.schemas.user import UserCreateSchema


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/get")
async def get_user(
    data: Annotated[LoginDTO, Depends()], ioc: Annotated[InteractorFactory, Depends()]
):
    async with ioc.authenticate() as interactor:
        return await interactor(data)


@router.post("/create")
async def create_user(
    data:  UserCreateSchema, ioc: Annotated[InteractorFactory, Depends()]
):
    async with ioc.register() as interactor:
        return await interactor(data)
