from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserBaseInDB(UserBase):
    id: int


class UserCreate(UserBase):
    password: str


class User(UserCreate, UserBaseInDB):
    pass
