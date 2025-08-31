import datetime

from pydantic import BaseModel, ConfigDict

from app.util.datetime_formatter import format_datetime_into_isoformat


class BaseSchemaModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        populate_by_name=True,
        json_encoders={datetime.datetime: format_datetime_into_isoformat}
    )