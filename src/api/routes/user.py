from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends

from src.schema.user import UserSchema
from src.api.deps import get_current_user

if TYPE_CHECKING:
    from src.models import User

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/me/")
async def profile(
        user: "User" = Depends(get_current_user)
) -> UserSchema:
    return UserSchema.from_orm(user)
