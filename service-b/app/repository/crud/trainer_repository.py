import sqlalchemy
from loguru import logger
from fastapi import HTTPException
from app.model.db.trainer import Trainer
from app.model.schemas.trainer_dto import TrainerDTO
from app.repository.crud.base import BaseCRUDRepository


class TrainerCRUDRepository(BaseCRUDRepository):

    async def read_trainer(self, trainer_id: int) -> TrainerDTO:
        logger.info(f"PROGRESS | Reading trainer {trainer_id} data in service B...")
        stmt = sqlalchemy.select(Trainer).where(Trainer.id == trainer_id)
        result = await self.async_session.execute(statement=stmt)
        trainer = result.scalar()

        if trainer is None:
            raise HTTPException(status_code=404, detail=f"Trainer with id {trainer_id} not found")

        logger.info(f"COMPLETE | Reading trainer {trainer_id} data in service B...")
        return TrainerDTO.from_orm(trainer)
