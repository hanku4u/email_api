from typing import List, Optional
from pydantic import BaseModel
from app.schemas.email_type import EmailType


# Model for users
class UserBase(BaseModel):
    name: Optional[str]
    email: Optional[str]

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    subscribed: bool
    email_types: List[EmailType] = []

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    pass


# Model for users and their subscribed email types
class UserEmailTypes(BaseModel):
    user: User
    email_types: List[EmailType] = []