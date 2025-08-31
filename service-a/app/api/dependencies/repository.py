from typing import Type, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession as SQLAlchemyAsyncSession

from app.api.dependencies.session import get_async_session
from app.repository.crud.base import BaseCRUDRepository


def get_repository(
    repo_type: Type[BaseCRUDRepository],
) -> Callable[[SQLAlchemyAsyncSession], BaseCRUDRepository]:
    """
    Factory function to create repository dependencies.

    Args:
        repo_type: The repository class to instantiate

    Returns:
        A dependency function that creates a repository instance
    """
    def _get_repo(
        async_session: SQLAlchemyAsyncSession = Depends(get_async_session),
    ) -> BaseCRUDRepository:
        return repo_type(async_session=async_session)

    return _get_repo