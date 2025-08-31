from typing import List

from app.model.schemas.base import BaseSchemaModel
from app.model.schemas.TrainerDTO import TrainerDTO

class PokemonDTO(BaseSchemaModel):
    id: int
    name: str
    type: List[str]
    hp: int
    attack: int
    defense: int
    speed: int
    generation: int

class PokemonTrainerDTO(BaseSchemaModel):
    trainer_data: TrainerDTO
    pokemon_data: PokemonDTO