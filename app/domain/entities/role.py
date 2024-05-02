from typing import List

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.application.common.db import Base


class Role(Base):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    permissions: Mapped[List[str]] = mapped_column(ARRAY(String))
