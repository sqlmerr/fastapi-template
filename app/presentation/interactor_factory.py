from abc import abstractmethod, ABC
from app.application.delete_post import DeletePost
from app.application.get_all_posts import GetAllPosts

from app.application.authenticate import Authenticate
from app.application.register import Register
from app.application.get_post import GetPost
from app.application.create_post import CreatePost
from app.application.update_post import UpdatePost


class InteractorFactory(ABC):
    @abstractmethod
    async def authenticate(
        self,
    ) -> Authenticate:
        raise NotImplementedError

    @abstractmethod
    async def register(self) -> Register:
        raise NotImplementedError

    @abstractmethod
    async def get_post(self) -> GetPost:
        raise NotImplementedError

    @abstractmethod
    async def get_all_posts(self) -> GetAllPosts:
        raise NotImplementedError

    @abstractmethod
    async def create_post(self) -> CreatePost:
        raise NotImplementedError

    @abstractmethod
    async def delete_post(self) -> DeletePost:
        raise NotImplementedError

    @abstractmethod
    async def update_post(self) -> UpdatePost:
        raise NotImplementedError
