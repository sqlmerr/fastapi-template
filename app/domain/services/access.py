from app.domain.exceptions.access import AccessDeniedError


class AccessService:
    def ensure_has_permissions(self, user_role_permissions: list[str], permissions: list[str]) -> None:
        if "*" in user_role_permissions:
            return

        for permission in permissions:
            if permission not in user_role_permissions:
                raise AccessDeniedError
