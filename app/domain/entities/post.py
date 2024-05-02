from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.application.common.db import Base
from .user import User


class Post(Base):
    __tablename__ = "post"

    text: Mapped[str]

    author_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    author: Mapped[User] = relationship()
