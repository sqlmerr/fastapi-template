from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from src.core.schemas import UserSchemaAdd
from src.core.unitofwork import IUnitOfWork
from src.core.services import UsersService
from src.dependencies import get_uow


router = APIRouter(prefix="/users")


@router.post("/create/")
async def create_user(
    user: UserSchemaAdd,
    uow: Annotated[IUnitOfWork, Depends(get_uow)]
):
    response = await UsersService().add_user(uow, user)
    if response is False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already exists")
    return {"status_code": status.HTTP_201_CREATED, "user_id": response}
