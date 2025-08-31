from sqlalchemy import Column, Integer, String, DateTime, func

from app.repository.table import Base

class Trainer(Base):
    __tablename__ = "trainers"
    __table_args__ = {"schema": "service_b"}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    region = Column(String(50), nullable=False)

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