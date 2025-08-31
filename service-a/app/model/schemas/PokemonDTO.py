from typing import List

from app.model.schemas.base import BaseSchemaModel


class PokemonDTO(BaseSchemaModel):
    id: int
    name: str
    type: List[str]
    hp: int
    attack: int
    defense: int
    speed: int
    generation: int
