from typing import Annotated
from jose.exceptions import JWTError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.utils.jwt import decode
from app.application.schemas.token import TokenData
from app.presentation.interactor_factory import InteractorFactory
from app.application.authenticate import LoginDTO
from app.application.schemas.user import UserSchema


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token/")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    ioc: Annotated[InteractorFactory, Depends()]
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
    except JWTError:
        raise credentials_exception
    async with ioc.authenticate() as interactor:
        user = await interactor(LoginDTO(username=token_data.username, password=None), False)
    if user is None:
        raise credentials_exception
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[UserSchema, Depends(get_current_user)]
