from typing import Any

from app.model.schemas.base import BaseSchemaModel


class OutputSchema(BaseSchemaModel):
    http_status: int
    error_code: str
    message: str

class GlobalResponse(BaseSchemaModel):
    output_schema: OutputSchema
    content: Any