from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from app.application.common.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    registered_at: Mapped[datetime]
