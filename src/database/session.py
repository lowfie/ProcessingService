from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    create_async_engine,
    async_sessionmaker
)

from src.config import settings

engine = create_async_engine(
    settings.POSTGRES_DSN,
    echo=False,
    echo_pool=False,
    pool_size=150,
    max_overflow=15,
    pool_pre_ping=True,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

async_session = async_scoped_session(async_session_factory, scopefunc=current_task)
