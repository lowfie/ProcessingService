import re
from datetime import datetime
from typing import Iterable, Sequence, Type

from sqlalchemy.sql import func
from sqlalchemy.sql.selectable import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql.expression import UnaryExpression
from sqlalchemy import delete, select, update, BigInteger
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class used for declarative class definitions.

    [T] - dynamic typing of database model classes
    """
    id: Mapped[str] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), default=func.now()
    )

    @declared_attr.directive
    def __tablename__(self) -> str:
        names = re.split("(?=[A-Z])", self.__name__)
        return "_".join([x.lower() for x in names if x])

    @classmethod
    async def _paginate_stmt[T: DeclarativeBase](
        cls: "Base" | Type[T],
        db: AsyncSession,
        stmt: Select,
        page: int | None = 1,
        per_page: int | None = 5,
    ) -> tuple[Sequence[T], int, int]:
        instances = await db.scalars(stmt)
        total_items = len(instances.all())
        total_pages = (total_items + per_page - 1) // per_page
        sub_stmt = stmt.offset((page - 1) * per_page).limit(per_page)
        instances = await db.scalars(sub_stmt)
        return instances.all(), total_pages, total_items

    def dict(
        self, include: Iterable | None = None, exclude: Iterable | None = None
    ) -> dict:
        if include is None:
            include = self.__dict__.keys()
        if exclude is None:
            exclude = set()
        return {attr: getattr(self, attr) for attr in include if attr not in exclude}

    @classmethod
    async def get[T: DeclarativeBase](
        cls: "Base" | Type[T], db: AsyncSession, id: str
    ) -> T | None:
        stmt = select(cls).where(cls.id == id)
        instance = await db.scalar(stmt)
        return instance

    @classmethod
    async def delete[T: DeclarativeBase](
            cls: "Base" | Type[T], db: AsyncSession, id: str
    ) -> None:
        stmt = delete(cls).where(cls.id == id)
        await db.execute(stmt)
        await db.flush()

    @classmethod
    async def get_by[T: DeclarativeBase](
        cls: "Base" | Type[T], db: AsyncSession, **kwargs
    ) -> T | None:
        stmt = select(cls).filter_by(**kwargs)
        instance = await db.scalar(stmt)
        return instance

    @classmethod
    async def get_multi[T: DeclarativeBase](
        cls: "Base" | Type[T],
        db: AsyncSession,
        skip: int | None = None,
        limit: int | None = None,
        **kwargs,
    ) -> Sequence[T]:
        stmt = select(cls).filter_by(**kwargs).offset(skip).limit(limit)
        instances = await db.scalars(stmt)
        return instances.all()

    @classmethod
    async def get_paginated_multi[T: DeclarativeBase](
        cls: "Base" | Type[T],
        db: AsyncSession,
        order_by: InstrumentedAttribute | UnaryExpression,
        page: int | None = 1,
        per_page: int | None = 5,
        **kwargs,
    ) -> tuple[Sequence[T], int, int]:
        stmt = select(cls).filter_by(**kwargs).order_by(order_by)
        return await cls._paginate_stmt(db=db, stmt=stmt, page=page, per_page=per_page)

    @classmethod
    async def get_all[T: DeclarativeBase](
            cls: "Base" | Type[T], db: AsyncSession
    ) -> Sequence[T]:
        stmt = select(cls)
        instances = await db.scalars(stmt)
        return instances.all()

    @classmethod
    async def create[T: DeclarativeBase](
            cls: "Base" | Type[T], db: AsyncSession, **kwargs
    ) -> T:
        instance = cls(**kwargs)
        db.add(instance)
        await db.flush()
        return instance

    @classmethod
    async def bulk_create[T: DeclarativeBase](
        cls: "Base" | Type[T], db: AsyncSession, dict_values: list[dict]
    ) -> None:
        instances = [cls(**values) for values in dict_values]
        db.add_all(instances)
        await db.flush()

    @classmethod
    async def get_or_create[T: DeclarativeBase](
        cls: "Base" | Type[T],
        db: AsyncSession,
        defaults: dict = None,
        **kwargs,
    ) -> tuple[T, bool]:
        instance = await cls.get_by(db=db, **kwargs)
        if instance:
            return instance, False
        else:
            params = dict(defaults or {}, **kwargs)
            return await cls.create(db=db, **params), True

    @classmethod
    async def update[T: DeclarativeBase](
        cls: "Base" | Type[T], db: AsyncSession, id: str, **kwargs
    ) -> None:
        stmt = update(cls).where(cls.id == id).values(**kwargs)
        await db.execute(stmt)
        await db.flush()

    @classmethod
    async def select_and_update[T: DeclarativeBase](
        cls: "Base" | Type[T],
        db: AsyncSession,
        id: str,
        **kwargs,
    ) -> T | None:
        instance = await cls.get(db=db, id=id)
        if instance:
            await cls.update(db=db, id=id, **kwargs)
        return instance

    @classmethod
    async def update_or_create[T: DeclarativeBase](
        cls: "Base" | Type[T], db: AsyncSession, defaults=None, **kwargs
    ) -> tuple[T, bool]:
        instance = await cls.get_by(db=db, **kwargs)
        if instance:
            await cls.update(db=db, id=instance.id, **defaults)
            return instance, False
        else:
            instance = await cls.create(db=db, **dict(defaults or {}, **kwargs))
            return instance, True
