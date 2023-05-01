from typing import List, Optional
from pydantic import BaseModel


# Model for email types
class EmailTypeBase(BaseModel):
    name: str

class EmailTypeCreate(EmailTypeBase):
    pass

class EmailType(EmailTypeBase):
    id: int

    class Config:
        orm_mode = True