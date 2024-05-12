from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_db
from src.services import auth, users
from src.schema import UserSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register/")
async def register_user(
        payload: auth.PayloadSchema,
        db: AsyncSession = Depends(get_db)
) -> UserSchema:
    user = await users.get_by(db=db, username=payload.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    user = await users.create(db=db, username=payload.username, password=payload.password)
    return UserSchema.from_orm(user)


@auth_router.post("/login/")
async def get_access_token(
        payload: auth.PayloadSchema,
        db: AsyncSession = Depends(get_db)
) -> auth.AccessTokenSchema:
    user = await users.get_by(db=db, username=payload.username, password=payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong username or password")

    access_token = auth.access_security.create_access_token(subject=payload.dict())
    return auth.AccessTokenSchema(access_token=access_token)
