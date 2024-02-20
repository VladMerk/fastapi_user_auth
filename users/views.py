from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from core.database import db
from users.models import Users
from users.schemas import User, UserCreate
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
async def delete_user(user_id: int = Path(...), session: Session = Depends(db.session_dependency)) -> User:
    return await db_users.remove(session=session, model_id=user_id)
