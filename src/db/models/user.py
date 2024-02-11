from sqlalchemy.orm import Mapped, mapped_column

from src.db.db import Base
from src.core.schemas import UserSchema


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)


    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            username=self.username
        )
