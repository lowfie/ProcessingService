from fastapi import APIRouter

from .receiver import receiver_router
from .healthcheck import healthcheck_router
from .user import user_router
from .auth import auth_router

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(user_router)
v1_router.include_router(auth_router)
v1_router.include_router(receiver_router)
v1_router.include_router(healthcheck_router)
