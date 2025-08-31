from loguru import logger
from app.model.schemas.GlobalResponse import GlobalResponse
from app.repository.proxy.base import BaseProxy


class ServiceAProxy(BaseProxy):

    async def get_potential_pokemon(self, trainer_id: int) -> GlobalResponse:
        logger.info(f"PROGRESS | Getting potential pokemon from service A {self.base_url}...")
        response = await self.client.get(f"/service-a/potential-pokemons/{trainer_id}")
        response.raise_for_status()
        logger.info(f"COMPLETE | Getting potential pokemon from service A - {response.status_code}...")
        return GlobalResponse(**response.json())