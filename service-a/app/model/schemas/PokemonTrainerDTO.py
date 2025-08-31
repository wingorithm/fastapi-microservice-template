from typing import List

from app.model.schemas.base import BaseSchemaModel
from app.model.schemas.PokemonDTO import PokemonDTO

class TrainerDTO(BaseSchemaModel):
    id: int
    name: str
    age: int
    region: str

class PokemonTrainerDTO(BaseSchemaModel):
    pokemon_data: PokemonDTO
    trainer_data: TrainerDTO
