from src.core.schemas import UserSchemaAdd, UserSchemaEdit
from src.core.unitofwork import IUnitOfWork


class UsersService:
    async def add_user(self, uow: IUnitOfWork, user: UserSchemaAdd):
        user_dict = user.model_dump()
        async with uow:
            if await uow.users.find_one(username=user.username):
                return False
            
            user_id = await uow.users.add_one(user_dict)
            await uow.commit()
            return user_id

    async def get_users(self, uow: IUnitOfWork):
        async with uow:
            users = await uow.users.find_all()
            return users
    
    async def get_user(self, id: int, uow: IUnitOfWork):
        async with uow:
            user = await uow.users.find_one(id=id)
            return user

    
    async def delete_user(self, id: int, uow: IUnitOfWork):
        async with uow:
            if not await uow.users.find_one(id=id):
                return False

            response = await uow.users.delete_one(id=id)
            await uow.commit()
            return response
        
    
    async def edit_user(self, id: int, user: UserSchemaEdit, uow: IUnitOfWork):
        user_dict = user.model_dump()
        async with uow:
            if not await uow.users.find_one(id=id):
                return False

            response = await uow.users.edit_one(id, user_dict)
            await uow.commit()
            return response
