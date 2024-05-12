from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.application.common.id_provider import IdProvider
from app.application.schemas import Token, UserCreateSchema, UserSchema
from app.application.user.authenticate import Authenticate, LoginDTO
from app.application.user.register import Register, RegisterDTO
from app.infrastructure.auth.jwt import JwtTokenProcessor
from app.infrastructure.auth.password import PasswordProcessor
from app.presentation.api.dependencies import OAuth2Depends

router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)


async def authenticate_user(
    username: str,
    password: str,
    interactor: Authenticate,
    password_processor: PasswordProcessor,
):
    user = await interactor(LoginDTO(id=None, username=username))
    if not user:
        return False
    if not password_processor.verify_password(password, user.password):
        return False
    return user


@router.post(
    "/token",
    responses={
        404: {"response": {"detail": "User not found"}},
        401: {"response": {"detail": "Incorrect username or password"}},
    },
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    interactor: FromDishka[Authenticate],
    token_processor: FromDishka[JwtTokenProcessor],
) -> Token:
    user = await interactor(LoginDTO(id=None, username=form_data.username, password=form_data.password))

    access_token = token_processor.create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token, token_type="Bearer")


@router.get("/profile", dependencies=[OAuth2Depends])
async def profile(interactor: FromDishka[Authenticate], id_provider: FromDishka[IdProvider]) -> UserSchema:
    return await interactor(LoginDTO(id=id_provider.get_current_user_id(), password=None), password_verify=False)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreateSchema,
    interactor: FromDishka[Register],
    password_processor: FromDishka[PasswordProcessor],
):
    data.password = password_processor.get_password_hash(data.password)
    result = await interactor(RegisterDTO(**data.model_dump()))
    if isinstance(result, bool):
        return {"status": result}
    return {"user_id": result}
