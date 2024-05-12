from fastapi import APIRouter, status, Depends
from fastapi.responses import Response

from src.models import User
from src.api.deps import get_current_user, get_admin

healthcheck_router = APIRouter(prefix="/healthcheck", tags=["healthcheck"])


@healthcheck_router.get("/unprotect/", response_model=str)
async def unprotect_healthcheck() -> Response:
    return Response(content="ok", status_code=status.HTTP_200_OK)


@healthcheck_router.get("/protect/", response_model=str)
async def protect_healthcheck(
        _: User = Depends(get_current_user)
) -> Response:
    return Response(content="ok", status_code=status.HTTP_200_OK)


@healthcheck_router.get("/admin_protect/", response_model=str)
async def admin_protect_healthcheck(
        _: User = Depends(get_admin)
) -> Response:
    return Response(content="ok", status_code=status.HTTP_200_OK)
