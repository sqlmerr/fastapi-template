from fastapi import FastAPI

from dishka import Provider, Scope, provide, make_async_container
from dishka.integrations.fastapi import (
    setup_dishka,
)

from app.ioc import InteractorFactory


class IocProvider(Provider):
    def __init__(self, ioc: InteractorFactory) -> None:
        self.ioc = ioc
        super().__init__()

    @provide(scope=Scope.APP)
    def get_ioc(self) -> InteractorFactory:
        return self.ioc


def init_di(app: FastAPI, ioc: InteractorFactory) -> None:
    container = make_async_container(IocProvider(ioc))
    setup_dishka(container, app)
