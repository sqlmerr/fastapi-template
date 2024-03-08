from typing import Annotated

from fastapi import APIRouter, Depends
from app.presentation.interactor_factory import InteractorFactory
from app.application.authenticate import LoginDTO
from app.application.schemas.user import UserCreateSchema

from dishka.integrations.fastapi import FromDishka, inject


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/get")
@inject
async def get_user(
    data: Annotated[LoginDTO, Depends()], ioc: Annotated[InteractorFactory, FromDishka()]
):
    async with ioc.authenticate() as interactor:
        return await interactor(data)


@router.post("/create")
@inject
async def create_user(
    data:  UserCreateSchema, ioc: Annotated[InteractorFactory, FromDishka()]
):
    async with ioc.register() as interactor:
        return await interactor(data)
