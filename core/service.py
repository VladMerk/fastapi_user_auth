from typing import Generic, Type, TypeVar

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, model_id: int, session: AsyncSession) -> ModelType:
        return await session.get(self.model, self.model.id == model_id)

    async def get_all(self, session: AsyncSession) -> list[ModelType]:
        result: ScalarResult = await session.scalars(select(self.model))
        return list(result.all())

    async def create(self, session: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(obj_in.model_dump())
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, session: AsyncSession, model_id: int) -> ModelType:
        obj: ModelType = await session.scalar(select(self.model).where(self.model.id == model_id))
        if obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id={model_id} not found")

        await session.delete(obj)
        await session.commit()
        return obj
