from dataclasses import dataclass, field
from uuid import UUID

from app.application.common.id_provider import IdProvider
from app.application.common.interactor import Interactor
from app.application.common.post_gateway import PostCreator
from app.application.common.user_gateway import UserReader
from app.application.schemas.post import PostSchemaCreate
from app.domain.services.access import AccessService


@dataclass(frozen=True)
class CreatePostDTO:
    data: PostSchemaCreate


@dataclass(frozen=True)
class CreatePost(Interactor[CreatePostDTO, UUID | bool]):
    post_creator: PostCreator
    user_reader: UserReader
    id_provider: IdProvider
    access_service: AccessService = field(default_factory=AccessService)

    async def __call__(self, data: CreatePostDTO) -> UUID | bool:
        user_id = self.id_provider.get_current_user_id()
        user_db = await self.user_reader.get_user(user_id, self.uow)
        self.access_service.ensure_has_permissions(user_db.role_permissions, ["posts:create"])

        data_dict = data.data.model_dump()
        result = await self.post_creator.create_post(data_dict, user_db, self.uow)

        return result
