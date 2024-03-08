from abc import abstractmethod, ABC

from app.application.authenticate import Authenticate
from app.application.register import Register


class InteractorFactory(ABC):
    @abstractmethod
    async def authenticate(
        self,
    ) -> Authenticate:
        raise NotImplementedError
    
    @abstractmethod
    async def register(
        self
    ) -> Register:
        raise NotImplementedError
