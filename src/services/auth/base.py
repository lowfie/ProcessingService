from datetime import timedelta

from fastapi_jwt import JwtAccessBearer

from src.config import config


access_security = JwtAccessBearer(
    secret_key=config.jwt.secret_key,
    algorithm=config.jwt.algorithm,
    auto_error=True,
    access_expires_delta=timedelta(days=1),
    refresh_expires_delta=timedelta(days=7)
)
