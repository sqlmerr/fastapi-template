from dataclasses import asdict, dataclass, field
from uuid import UUID

from app.application.common.id_provider import IdProvider
from app.application.common.interactor import Interactor
from app.application.common.role_gateway import RoleCreator
from app.application.common.user_gateway import UserReader
from app.domain.services.access import AccessService


@dataclass(frozen=True)
class CreateRoleDTO:
    name: str
    description: str
    permissions: list[str]


@dataclass(frozen=True)
class CreateRole(Interactor[CreateRoleDTO, UUID | None]):
    role_creator: RoleCreator
    user_reader: UserReader
    id_provider: IdProvider
    access_service: AccessService = field(default_factory=AccessService)

    async def __call__(self, data: CreateRoleDTO) -> UUID | None:
        user_id = self.id_provider.get_current_user_id()
        user = await self.user_reader.get_user(user_id, self.uow)
        self.access_service.ensure_has_permissions(user.role_permissions, ["roles:create"])

        role_id = await self.role_creator.create_role(asdict(data), self.uow)
        await self.uow.commit()
        return role_id
