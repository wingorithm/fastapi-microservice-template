import loguru
import pydantic
from sqlalchemy.ext.asyncio import (
    AsyncSession as SQLAlchemyAsyncSession,
    AsyncEngine as SQLAlchemyAsyncEngine,
    create_async_engine as create_sqlalchemy_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import Pool as SQLAlchemyPool, QueuePool as SQLAlchemyQueuePool

from app.config.manager import settings


class AsyncDatabase:
    def __init__(self):
        self.postgres_uri: pydantic.PostgresDsn = f"{settings.DB_POSTGRES_SCHEMA}://{settings.DB_POSTGRES_USERNAME}:{settings.DB_POSTGRES_PASSWORD}@{settings.DB_POSTGRES_HOST}:{settings.DB_POSTGRES_PORT}/{settings.DB_POSTGRES_NAME}"
        
        self.async_engine: SQLAlchemyAsyncEngine = create_sqlalchemy_async_engine(
            url=self.set_async_db_uri,
            echo=settings.IS_DB_ECHO_LOG,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_POOL_OVERFLOW,
            poolclass=SQLAlchemyQueuePool,
        )
        
        # Create async session factory
        self.async_session_factory = sessionmaker(
            bind=self.async_engine,
            class_=SQLAlchemyAsyncSession,
            expire_on_commit=False
        )
        
        self.pool: SQLAlchemyPool = self.async_engine.pool

    @property
    def set_async_db_uri(self) -> str:
        """
        Set the synchronous database driver into asynchronous version by utilizing AsyncPG:
            `postgresql://` => `postgresql+asyncpg://`
        """
        async_db_url = self.postgres_uri.replace("postgresql://", "postgresql+asyncpg://") if self.postgres_uri else self.postgres_uri
        loguru.logger.info(f"New Async DB Connection : {async_db_url}")
        return async_db_url
    
    async def get_session(self) -> SQLAlchemyAsyncSession:
        """Get an async session for database operations"""
        async with self.async_session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

async_db: AsyncDatabase = AsyncDatabase()