from typing import Type, TypeVar, Generic

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from .database import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, model_id: int, session: AsyncSession) -> ModelType:
        return await session.get(self.model, self.model.id == model_id)

    async def create(self, session: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(obj_in.model_dump())
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, session: AsyncSession, model_id: int) -> ModelType:
        obj: ModelType = await session.scalar(self.model, self.model.id == model_id)
        await session.delete(obj)
        await session.commit()
        return obj
