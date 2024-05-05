from dataclasses import dataclass
from uuid import UUID

from app.application.common.interactor import Interactor
from app.application.common.post_gateway import PostCreator
from app.application.common.uow import UoW
from app.application.common.user_gateway import UserReader
from app.application.schemas.post import PostSchemaCreate
from app.application.schemas.user import UserSchema


@dataclass(frozen=True)
class CreatePostDTO:
    data: PostSchemaCreate
    user: UserSchema


class CreatePost(Interactor[CreatePostDTO, UUID | bool]):
    def __init__(
        self, uow: UoW, post_creator: PostCreator, user_reader: UserReader
    ) -> None:
        self.uow = uow
        self.post_creator = post_creator
        self.user_reader = user_reader

    async def __call__(self, data: CreatePostDTO) -> UUID | bool:
        data_dict = data.data.model_dump()
        user_db = await self.user_reader.get_user(data.user.id, self.uow)
        result = await self.post_creator.create_post(data_dict, user_db, self.uow)

        return result
