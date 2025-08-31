from loguru import logger
from app.model.schemas.GlobalResponse import GlobalResponse
from app.repository.proxy.base import BaseProxy


class ServiceBProxy(BaseProxy):

    async def get_potential_trainer(self, pokemon_id: int) -> GlobalResponse:
        logger.info(f"PROGRESS | Getting potential pokemon from service A {self.base_url}...")
        response = await self.client.get(f"/service-b/potential-trainer/{pokemon_id}")
        response.raise_for_status()
        logger.info(f"COMPLETE | Getting potential trainer from service A - {response.status_code}...")
        return GlobalResponse(**response.json())