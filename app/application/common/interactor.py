from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from .uow import UoW

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


@dataclass(frozen=True)
class Interactor(Generic[InputDTO, OutputDTO]):
    uow: UoW

    async def __call__(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError


InteractorT = TypeVar("InteractorT")
InteractorFactory = Callable[[], InteractorT]
