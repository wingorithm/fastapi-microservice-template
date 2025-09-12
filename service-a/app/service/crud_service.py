import random
from typing import Any, Coroutine

from loguru import logger

from app.model.schemas.global_response import GlobalResponse
from app.model.schemas.pokemon_dto import PokemonDTO
from app.model.schemas.pokemon_trainer_dto import PokemonTrainerDTO
from app.repository.crud.pokemon_repository import PokemonCRUDRepository
from app.repository.proxy.service_b_proxy import ServiceBProxy


class CrudService:
    def __init__(
            self,
            crud_repo: PokemonCRUDRepository,
            service_b_proxy: ServiceBProxy
    ):
        self.crud_repo = crud_repo
        self.service_b_proxy = service_b_proxy

    async def get_random_pokemon(self) -> PokemonTrainerDTO:
        try:
            logger.info("PROGRESS | Getting random pokemon in service A...")
            pokemon:PokemonDTO= await self.crud_repo.read_pokemon(random.randint(1, 10))
            potential_trainer:GlobalResponse = await self.service_b_proxy.get_potential_trainer(random.randint(1, 5))

            return PokemonTrainerDTO(
                pokemon_data=pokemon,
                trainer_data=potential_trainer.content,
            )
        except Exception as e:
            logger.error(f"Something Error on CurdService.get_random_pokemon | {e}")
            raise

    async def get_pokemon(self, trainer_id: int) -> PokemonDTO:
        try:
            logger.info("PROGRESS | Getting random pokemon in service A...")
            return await self.crud_repo.read_pokemon(trainer_id)
        except Exception as e:
            logger.error(f"Something Error on CurdService.get_pokemon | {e}")
            raise