import contextlib
import typing

from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession

from app.repository.database import async_db


async def get_async_session() -> typing.AsyncGenerator[SQLAlchemyAsyncSession, None]:
    """
    Dependency function that yields an async database session.
    """
    async with async_db.async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            print(f"Database session error: {e}")
            await session.rollback()
            raise  # Re-raise the exception after rollback
        finally:
            await session.close()


# Optional: Context manager for use in non-FastAPI contexts
@contextlib.asynccontextmanager
async def async_session_context() -> typing.AsyncGenerator[SQLAlchemyAsyncSession, None]:
    """
    Async context manager for database sessions.
    Usage:
        async with async_session_context() as session:
            # do database operations
    """
    async with async_db.async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            print(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


def get_db_dependency() -> typing.Callable:
    """
    Returns a FastAPI dependency for database sessions.
    Usage:
        @app.get("/endpoint")
        async def endpoint(db: SQLAlchemyAsyncSession = Depends(get_db_dependency())):
            # do database operations
    """
    async def _get_db() -> typing.AsyncGenerator[SQLAlchemyAsyncSession, None]:
        async with async_db.async_session_factory() as session:
            try:
                yield session
            except Exception as e:
                print(f"Database session error: {e}")
                await session.rollback()
                raise
            finally:
                await session.close()
    
    return _get_db