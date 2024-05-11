from .base import DomainException


class AccessDeniedError(DomainException):
    pass


class AuthenticationError(DomainException):
    pass
