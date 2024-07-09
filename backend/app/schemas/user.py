from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    spotify_user_id: str
    username: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    images: Optional[str] = None
    profile_url: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
