from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base

if TYPE_CHECKING:
    from src.models import User


class Receive(Base):
    timestamp: Mapped[int] = mapped_column(BigInteger)

    a: Mapped[int | None]
    b: Mapped[int | None]
    c: Mapped[int | None]
    d: Mapped[int | None]
    e: Mapped[int | None]
    f: Mapped[int | None]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(foreign_keys=[user_id], lazy="subquery")
