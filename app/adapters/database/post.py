from typing import Optional, Union
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import OperationalError

from app.application.common.post_gateway import PostCreator, PostDeleter, PostReader, PostUpdater
from app.application.common.uow import UoW
from app.domain.entities.post import Post
from app.domain.entities.user import User


class PostGateway(PostReader, PostCreator, PostDeleter, PostUpdater):
    async def get_post(self, post_id: UUID, uow: UoW) -> Optional[Post]:
        stmt = select(Post).where(Post.id == post_id)
        result = await uow.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_posts(self, author_id: UUID, uow: UoW) -> list[Post]:
        stmt = select(Post).where(Post.author_id == author_id)
        result = await uow.session.execute(stmt)
        return result.all()

    async def create_post(self, data: dict, author: User, uow: UoW) -> Optional[Union[int, bool]]:
        try:
            stmt = insert(Post).values(**data, author_id=author.id).returning(Post.id)
            result = await uow.session.execute(stmt)
        except OperationalError:
            stmt = insert(Post).values(**data, author_id=author.id)
            await uow.session.execute(stmt)
        await uow.commit()
        return True or result.scalar_one_or_none()

    async def delete_post(self, post_id: UUID, uow: UoW) -> bool:
        stmt = delete(Post).where(Post.id == post_id)
        await uow.session.execute(stmt)
        await uow.commit()
        return True

    async def update_post(self, post_id: UUID, data: dict, uow: UoW) -> bool:
        stmt = update(Post).where(Post.id == post_id).values(**data)
        await uow.session.execute(stmt)
        await uow.commit()
        return True
