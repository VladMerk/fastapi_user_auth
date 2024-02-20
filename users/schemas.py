from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserBaseInDB(UserBase):
    id: int


class UserCreate(UserBaseInDB):
    password: str


class User(UserBaseInDB):
    pass
