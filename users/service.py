from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.service import CRUDBase
from users.models import Users
from users.schemas import UserCreate
from users.utils import hash_password, verify_password


class CRUDUsers(CRUDBase[Users, UserCreate]):

    async def get_by_email(self, session: AsyncSession, email: str) -> Users | None:
        return await session.scalar(select(self.model).where(self.model.email == email))

    async def create(self, session: AsyncSession, user_in: UserCreate) -> Users:
        user = Users(email=user_in.email, password=hash_password(user_in.password))
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def authenticate(self, session: AsyncSession, email: str, password: str) -> Users | None:
        user: Users = await self.get_by_email(session=session, email=email)
        if not user:
            return None
        if not verify_password(plain_password=password, hashed_password=user.password):
            return None
        return user


db_users = CRUDUsers(Users)
