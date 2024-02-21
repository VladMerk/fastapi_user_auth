from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from core.database import db
from core.settings import settings
from users.models import Users
from users.schemas import User, UserCreate
from users.security import get_current_user, get_current_active_user
from users.service import db_users

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[User])
async def get_users(session: Session = Depends(db.session_dependency)) -> list[User]:
    return await db_users.get_all(session=session)


@router.post("/", response_model=User)
async def create_user(user_in: UserCreate, session: Session = Depends(db.session_dependency)) -> User:
    user_in_db: Users | None = await db_users.get_by_email(session=session, email=user_in.email)
    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="The user with that email already in the database"
        )
    user: Users = await db_users.create(session=session, user_in=user_in)
    return User.model_validate(user)


@router.delete("/{user_id}", response_model=User)
async def delete_user(
    user_id: int = Path(...),
    session: Session = Depends(db.session_dependency),
    user: Users = Depends(get_current_active_user),
) -> User:
    return await db_users.remove(session=session, model_id=user_id)


@router.post("/login")
async def login_users(
    form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(db.session_dependency)
):
    user: Users = await db_users.authenticate(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload: dict = {
        "sub": form_data.username,
        "email": form_data.username,
        "password": form_data.password,
        "exp": datetime.utcnow() + timedelta(minutes=settings.access_token_expires_minutes),
        "iat": datetime.utcnow(),
    }
    encoded_jwt = jwt.encode(payload, settings.private_key_path.read_text(), algorithm=settings.algorithm)
    return {"access_token": encoded_jwt, "token_type": "Bearer"}


@router.get("/me", response_model=User)
async def read_user(user: User = Depends(get_current_user)) -> User:
    return user
