from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    id: str
    username: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    images: Optional[str] = None
    profile_url: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    created_at: datetime

    class Config:
        from_attributes = True
