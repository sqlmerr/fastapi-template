from typing import Annotated

from fastapi import APIRouter, Depends, status
from app.presentation.interactor_factory import InteractorFactory
from app.application.authenticate import LoginDTO
from app.application.schemas.user import UserCreateSchema, UserSchema

from dishka.integrations.fastapi import FromDishka, inject


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/get", response_model=UserSchema)
@inject
async def get_user(
    data: Annotated[LoginDTO, Depends()],
    ioc: Annotated[InteractorFactory, FromDishka()],
):
    async with ioc.authenticate() as interactor:
        return await interactor(data)


@router.post("/create", status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    data: UserCreateSchema, ioc: Annotated[InteractorFactory, FromDishka()]
):
    async with ioc.register() as interactor:
        return {"status": await interactor(data)}
