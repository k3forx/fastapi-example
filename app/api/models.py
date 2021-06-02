from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    id: int
    username: str
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str
    created_at: datetime


class UserBeforeRegister(BaseModel):
    username: str
    raw_password: str


class Note(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
