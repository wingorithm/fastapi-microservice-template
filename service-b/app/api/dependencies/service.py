from fastapi.params import Depends

from app.api.dependencies.repository import get_repository
from app.config.manager import settings
from app.repository.crud.trainer_repository import TrainerCRUDRepository
from app.repository.proxy.service_a_proxy import ServiceAProxy
from app.service.crud_service import CrudService

"""
This file act as Factory function to create service dependencies.

-> encapsulate the creation logic for service objects.
-> provides a central place to handle the initialization of complex objects.
"""

def get_crud_service(
    crud_repo: TrainerCRUDRepository = Depends(get_repository(repo_type=TrainerCRUDRepository)),
) -> CrudService:
    """ dependencies for Crud service """
    return CrudService(
        crud_repo=crud_repo,
        service_a_proxy=ServiceAProxy(base_url=settings.SERVICE_A_URL)
    )