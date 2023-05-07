from typing import List, Optional
from pydantic import BaseModel
from app.schemas.email_type import EmailType


# Model for users
class UserBase(BaseModel):
    ghr_id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    dept_name: Optional[str]
    status: Optional[str]
    title: Optional[str]
    email: Optional[str]
    hashed_pw: Optional[str]
    subscribed: Optional[bool]


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    first_name: Optional[str]
    last_name: Optional[str]
    dept_name: Optional[str]
    status: Optional[str]
    title: Optional[str]
    email: Optional[str]


class User(UserBase):
    id: int
    ghr_id: str
    first_name: str
    last_name: str
    dept_name: str
    title: str
    subscribed: bool
    email_types: List[EmailType] = []

    class Config:
        orm_mode = True


# Model for users and their subscribed email types
class UserEmailTypes(BaseModel):
    user: User
    email_types: List[EmailType] = []


class UserLogin(BaseModel):
    email: str
    password: str