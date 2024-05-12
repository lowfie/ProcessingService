from sqlalchemy.ext.asyncio import AsyncSession

from src import models


async def create(db: AsyncSession, username: str, password: str) -> models.User:
    return await models.User.create(db=db, username=username, password=password)


async def get_by(db: AsyncSession, **kwargs) -> models.User:
    return await models.User.get_by(db=db, **kwargs)


async def get_or_create(db: AsyncSession, username: str, password: str) -> models.User:
    user = await get_by(db=db, username=username)
    if not user:
        user = await create(db=db, username=username, password=password)
    return user
