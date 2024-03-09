from typing import TypeVar, Callable
from fastapi import FastAPI

from dishka import (
    Provider,
    Scope,
    provide,
    make_async_container
)
from dishka.integrations.fastapi import (
    setup_dishka,
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


def init_di(app: FastAPI, ioc: InteractorFactory) -> None:
    container = make_async_container(IocProvider(ioc))
    setup_dishka(container, app)

    app.dependency_overrides.update(
        {
            InteractorFactory: singleton(ioc)
        }
    )
