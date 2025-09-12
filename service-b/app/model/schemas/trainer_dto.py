from app.model.schemas.base import BaseSchemaModel

class TrainerDTO(BaseSchemaModel):
    id: int
    name: str
    age: int
    region: str
