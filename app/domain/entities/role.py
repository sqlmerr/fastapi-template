from sqlalchemy.orm import Mapped

from app.application.common.db import Base


class Role(Base):
    __tablename__ = "role"

    name: Mapped[str]
    description: Mapped[str]
    permissions: Mapped[list[str]]
