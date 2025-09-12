import random

from loguru import logger

from app.model.schemas.global_response import GlobalResponse
from app.model.schemas.pokemon_trainer_dto import PokemonTrainerDTO
from app.model.schemas.trainer_dto import TrainerDTO
from app.repository.crud.trainer_repository import TrainerCRUDRepository
from app.repository.proxy.service_a_proxy import ServiceAProxy


class CrudService:
    def __init__(
            self,
            crud_repo: TrainerCRUDRepository,
            service_a_proxy: ServiceAProxy,
    ):
        self.crud_repo = crud_repo
        self.service_a_proxy = service_a_proxy

    async def get_random_trainer(self) -> PokemonTrainerDTO:
        try:
            logger.info("PROGRESS | Getting random trainer in service B...")
            trainer:TrainerDTO = await self.crud_repo.read_trainer(random.randint(1, 5))
            potential_pokemon:GlobalResponse = await self.service_a_proxy.get_potential_pokemon(trainer.id)

            return PokemonTrainerDTO(
                trainer_data=trainer,
                pokemon_data=potential_pokemon.content,
            )
        except Exception as e:
            logger.error(f"Something Error on CurdService.get_random_trainer | {e}")
            raise

    async def get_trainer(self, pokemon_id: int) -> TrainerDTO:
        try:
            logger.info("PROGRESS | Getting random trainer in service B...")
            return await self.crud_repo.read_trainer(pokemon_id)
        except Exception as e:
            logger.error(f"Something Error on CurdService.get_trainer | {e}")
            raise