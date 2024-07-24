from typing import Union

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class TokenBase(BaseModel):
    token: str

class TokenCreate(TokenBase):
    user_id: int


class Token(TokenCreate):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserAuth(UserBase):
    password: str

class UserCreate(UserAuth):
    username: str
    fullname: str

class User(UserBase):
    id: int
    is_active: bool = True
    username: str
    fullname: str
    items: list[Item] = []
    tokens: list[Token] = []

    class Config:
        orm_mode = True