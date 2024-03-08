from typing import TypeVar, Callable

from dishka import (
    Provider,
    Scope,
    provide,
)

from app.ioc import InteractorFactory


DependencyT = TypeVar("DependencyT")


def singleton(value: DependencyT) -> Callable[[], DependencyT]:
    """Produce save value as a fastapi dependency."""

    def singleton_factory() -> DependencyT:
        return value

    return singleton_factory


class IocProvider(Provider):
    def __init__(self, ioc: InteractorFactory) -> None:
        self.ioc = ioc
        super().__init__()

    @provide(scope=Scope.REQUEST)
    def get_ioc(self) -> InteractorFactory:
        return self.ioc
