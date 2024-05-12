from datetime import datetime, timedelta

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src import models


async def create(db: AsyncSession, **kwargs) -> models.Receive:
    return await models.Receive.create(db=db, **kwargs)


async def get_paginated_multi(
        db: AsyncSession,
        page: int = 1,
        per_page: int = 5,
        **kwargs
):
    return await models.Receive.get_paginated_multi(
        db=db,
        page=page,
        per_page=per_page,
        order_by=models.Receive.created_at.desc(),
        **kwargs
    )


async def total_receivers(db: AsyncSession, seconds: int):
    period = (datetime.now() - timedelta(seconds=seconds)).timestamp()

    stmt = (
        select(
            models.Receive.user_id,
            func.sum(models.Receive.a).label("total_a"),
            func.sum(models.Receive.b).label("total_b"),
            func.sum(models.Receive.c).label("total_c"),
            func.sum(models.Receive.d).label("total_d"),
            func.sum(models.Receive.e).label("total_e"),
            func.sum(models.Receive.f).label("total_f"),
        )
        .group_by(models.Receive.user_id)
        .where(models.Receive.timestamp >= period)
    )
    results = await db.execute(stmt)
    return results.all()
