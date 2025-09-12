from fastapi.params import Depends

from app.api.dependencies.repository import get_repository
from app.config.manager import settings
from app.repository.crud.pokemon_repository import PokemonCRUDRepository
from app.repository.proxy.service_b_proxy import ServiceBProxy
from app.service.crud_service import CrudService

"""
This file act as Factory function to create service dependencies.

-> encapsulate the creation logic for service objects.
-> provides a central place to handle the initialization of complex objects.
"""

def get_crud_service(
    crud_repo: PokemonCRUDRepository = Depends(get_repository(repo_type=PokemonCRUDRepository)),
) -> CrudService:
    """ dependencies for agent service """
    return CrudService(
        crud_repo=crud_repo,
        service_b_proxy=ServiceBProxy(base_url=settings.SERVICE_B_URL)
    )

