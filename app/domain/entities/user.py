from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.application.common.db import Base

from .role import Role


class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False, nullable=True)
    registered_at: Mapped[datetime]

    role_id: Mapped[UUID] = mapped_column(ForeignKey("role.id"))
    role: Mapped[Role] = relationship()
