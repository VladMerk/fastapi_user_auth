import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db
from core.settings import settings
from users.models import Users
from users.service import db_users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(db.session_dependency)
) -> Users:
    try:
        payload: dict = jwt.decode(token, settings.public_key_path.read_text(), algorithms=[settings.algorithm])
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Signature expired.")
    user: Users = await db_users.get_by_email(session=session, email=payload.get("email"))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


async def get_current_active_user(user: Users = Depends(get_current_user)):
    if user.is_active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User inactive or deleted.")
