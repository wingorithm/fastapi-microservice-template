import sqlalchemy
from loguru import logger

from app.model.db.Pokemon import Pokemon
from app.model.schemas.PokemonDTO import PokemonDTO
from app.repository.crud.base import BaseCRUDRepository


class PokemonCRUDRepository(BaseCRUDRepository):

    async def read_pokemon(self, pokemon_id: int) -> PokemonDTO:
        logger.info(f"PROGRESS | Reading pokemon {pokemon_id} data in service A...")
        stmt = sqlalchemy.select(Pokemon).where(Pokemon.id == pokemon_id)
        result = await self.async_session.execute(statement=stmt)
        poke = result.scalar()

        logger.info(f"COMPLETE | Reading pokemon {pokemon_id} data in service A...")
        return PokemonDTO.from_orm(poke)
