from typing import Annotated
from jwt.exceptions import PyJWTError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.utils.jwt import decode
from app.application.schemas.token import TokenData
from app.application.authenticate import LoginDTO, Authenticate
from app.application.schemas.user import UserSchema

from dishka.integrations.fastapi import FromDishka, inject


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


@inject
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    interactor: FromDishka[Authenticate],
):
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


CurrentUser = Annotated[UserSchema, Depends(get_current_user)]
