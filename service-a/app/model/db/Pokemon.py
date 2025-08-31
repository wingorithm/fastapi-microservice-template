from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.dialects.postgresql import ARRAY

from app.repository.table import Base

class Pokemon(Base):
    __tablename__ = "pokemons"
    __table_args__ = {'schema': 'service_a'}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(ARRAY(String), nullable=False)
    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    generation = Column(Integer, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now()
    )

    __mapper_args__ = {"eager_defaults": True}