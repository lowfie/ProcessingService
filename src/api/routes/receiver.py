from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.services import receivers
from src.schema.receiver import ReceiverSchema
from src.api.deps import get_current_user, get_db, get_admin

receiver_router = APIRouter(prefix="/receiver", tags=["receiver"])


@receiver_router.post("/")
async def receive_data(
        receive: receivers.ReceiverRequestSchema,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
) -> ReceiverSchema:
    instance = await receivers.create(db=db, user_id=user.id, **receive.dict())
    return ReceiverSchema.from_orm(instance)


@receiver_router.get("/all/")
async def get_receivers(
        user_id: int = Query(...),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=5, ge=1),
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_admin)
) -> receivers.ReceiversSchema:
    instances, total_pages, total_items = await receivers.get_paginated_multi(
        db=db,
        page=page,
        per_page=per_page,
        user_id=user_id,
    )
    return receivers.ReceiversSchema(
        receivers=instances,
        total_pages=total_pages,
        total_items=total_items,
    )


@receiver_router.get("/all/users/")
async def get_receivers(
        period: int = Query(
            ..., ge=1,
            le=int(datetime.now().timestamp()),
            description="Time interval per seconds"
        ),
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_admin)
) -> list[receivers.ReceiversUsersSchema]:
    return await receivers.total_receivers(db=db, seconds=period)
