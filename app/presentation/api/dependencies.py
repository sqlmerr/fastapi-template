from dataclasses import dataclass
from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError

from app.application.authenticate import Authenticate, LoginDTO
from app.application.get_role import GetRole
from app.application.schemas.token import TokenData
from app.application.schemas.user import UserSchema
from app.utils.jwt import decode

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


async def get_user(token: str, interactor: Authenticate) -> UserSchema | None:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = await interactor(
        LoginDTO(username=token_data.username, password=None), False
    )
    if user is None:
        raise credentials_exception
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user


@inject
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    interactor: FromDishka[Authenticate],
):
    return await get_user(token, interactor)


def get_current_user_with_permissions(permissions: list[str]):
    @inject
    async def get_user_with_permissions(
        token: Annotated[str, Depends(oauth2_scheme)],
        authenticate: FromDishka[Authenticate],
        get_role: FromDishka[GetRole],
    ) -> UserSchema | None:
        user = await get_user(token, authenticate)
        role = await get_role(user.role_id)
        exc = HTTPException(status.HTTP_403_FORBIDDEN, "You cannot do this")

        if "*" in role.permissions:
            return user

        for permission in permissions:
            if permission not in role.permissions:
                raise exc

        return user

    return get_user_with_permissions


CurrentUser = Annotated[UserSchema, Depends(get_current_user)]


# @dataclass(frozen=True)
# class CurrentUserWithPermissions:
#     permissions: list[str]
#
#     async def __call__(self, token: Annotated[str, Depends(oauth2_scheme)], ):
#
# CurrentUserWithPermissions = get_user_with_permissions
