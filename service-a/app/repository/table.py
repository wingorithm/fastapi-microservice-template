import typing
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

metadata = MetaData(schema="service_a")

Base: typing.Type[sqlalchemy.ext.declarative.DeclarativeMeta] = declarative_base(metadata=metadata)