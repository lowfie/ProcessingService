import uvicorn

from src.config import settings

if __name__ == '__main__':
    uvicorn.run(
        app="src.api.app:app",
        use_colors=settings.UVICORN_USE_COLORS,
        reload=settings.UVICORN_RELOAD,
        access_log=settings.UVICORN_ACCESS_LOG,
        workers=settings.UVICORN_WORKERS,
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        forwarded_allow_ips=settings.UVICORN_FORWARDED_ALLOW_IPS,
        proxy_headers=settings.UVICORN_PROXY_HEADERS
    )
