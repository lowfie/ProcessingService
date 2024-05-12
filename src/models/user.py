from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(256), default="", server_default="")
    password: Mapped[str]

    is_admin: Mapped[bool] = mapped_column(default=False, server_default="f")

    def __str__(self) -> str:
        return f"{self.username}"
