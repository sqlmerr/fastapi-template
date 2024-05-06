from dataclasses import dataclass
from uuid import UUID

from app.application.common.interactor import Interactor
from app.application.common.post_gateway import PostCreator
from app.application.common.user_gateway import UserReader
from app.application.schemas.post import PostSchemaCreate
from app.application.schemas.user import UserSchema


@dataclass(frozen=True)
class CreatePostDTO:
    data: PostSchemaCreate
    user: UserSchema


@dataclass(frozen=True)
class CreatePost(Interactor[CreatePostDTO, UUID | bool]):
    post_creator: PostCreator
    user_reader: UserReader

    async def __call__(self, data: CreatePostDTO) -> UUID | bool:
        data_dict = data.data.model_dump()
        user_db = await self.user_reader.get_user(data.user.id, self.uow)
        result = await self.post_creator.create_post(data_dict, user_db, self.uow)

        return result
