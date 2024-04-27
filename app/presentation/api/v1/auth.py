from datetime import timedelta
from typing import Annotated

from fastapi import Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm

from app.application.schemas.user import UserSchema, UserCreateSchema
from app.application.schemas.token import Token
from app.presentation.interactor_factory import InteractorFactory
from app.application.authenticate import LoginDTO
from app.utils.jwt import get_password_hash, verify_password, create_access_token
from app.presentation.api.dependencies import CurrentUser

from dishka.integrations.fastapi import FromDishka, inject


router = APIRouter(prefix="/auth", tags=["auth"])


async def authenticate_user(username: str, password: str, ioc: InteractorFactory):
    async with ioc.authenticate() as interactor:
        user = await interactor(LoginDTO(username=username))
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


@router.post("/token/")
@inject
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ioc: FromDishka[InteractorFactory],
) -> Token:
    async with ioc.authenticate() as interactor:
        user = await interactor(
            LoginDTO(username=form_data.username, password=form_data.password)
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/profile/", response_model=UserSchema)
async def profile(current_user: CurrentUser):
    return current_user


@router.post("/register/", status_code=status.HTTP_201_CREATED)
@inject
async def register(data: UserCreateSchema, ioc: FromDishka[InteractorFactory]):
    data.password = get_password_hash(data.password)
    async with ioc.register() as interactor:
        return {"status": await interactor(data)}
