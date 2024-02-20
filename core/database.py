from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from core.settings import settings


class Database:

    def __init__(self, db_url: str, db_echo: bool = False):
        self.engine = create_async_engine(url=db_url, echo=db_echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()


class Base(DeclarativeBase):
    __abstract__ = True


db = Database(db_url=settings.DB_URL, db_echo=False)
