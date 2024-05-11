from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class IdProvider(Protocol):
    @abstractmethod
    def get_current_user_id(self) -> UUID:
        raise NotImplementedError
