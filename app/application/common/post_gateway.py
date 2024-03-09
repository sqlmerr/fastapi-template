from abc import abstractmethod
from typing import Protocol, Optional, Union

from app.domain.entities.post import Post
from app.application.common.uow import UoW
from app.domain.entities.user import User


class PostReader(Protocol):
    @abstractmethod
    async def get_post(self, post_id: int, uow: UoW) -> Optional[Post]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_posts(self, user_id: int, uow: UoW) -> list[Post]:
        raise NotImplementedError


class PostCreator(Protocol):
    @abstractmethod
    async def create_post(
        self, data: dict, author: User, uow: UoW
    ) -> Optional[Union[int, bool]]:
        raise NotImplementedError


class PostDeleter(Protocol):
    @abstractmethod
    async def delete_post(self, post_id: int, uow: UoW) -> bool:
        raise NotImplementedError


class PostUpdater(Protocol):
    @abstractmethod
    async def update_post(self, post_id: int, data: dict, uow: UoW) -> bool:
        raise NotImplementedError
