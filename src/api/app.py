from fastapi import FastAPI

from .routes import v1_router


def setup_app() -> FastAPI:
    app = FastAPI(
        title="Handler Service",
        docs_url="/api/v1/docs",
        openapi_url="/api/openapi.json",
    )
    app.include_router(v1_router)

    return app


app = setup_app()
