from typing import AsyncGenerator, TYPE_CHECKING

from fastapi import Security, Depends, status, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import auth, users
from src.database.actions import db_session

if TYPE_CHECKING:
    from src.models import User


async def get_db() -> AsyncGenerator:
    async with db_session() as db:
        yield db


async def get_current_user(
        credentials: JwtAuthorizationCredentials = Security(auth.access_security),
        db: AsyncSession = Depends(get_db)
) -> "User":
    user = await users.get_by(
        db=db,
        username=credentials.subject.get("username"),
        password=credentials.subject.get("password"),
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user


async def get_admin(
        user: "User" = Depends(get_current_user)
) -> "User":
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not administrator"
        )
    return user
