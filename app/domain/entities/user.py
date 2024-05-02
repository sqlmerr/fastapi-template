from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.application.common.db import Base


class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False, nullable=True)
    registered_at: Mapped[datetime]
