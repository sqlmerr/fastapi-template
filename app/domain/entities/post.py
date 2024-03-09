from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from app.application.common.db import Base
from .user import User


class Post(Base):
    __tablename__ = "posts"

    text: Mapped[str]

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped[User] = relationship()
