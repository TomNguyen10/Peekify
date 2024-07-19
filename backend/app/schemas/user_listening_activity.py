from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserListeningActivityBase(BaseModel):
    activity_listened_at: datetime


class UserListeningActivityCreate(UserListeningActivityBase):
    spotify_user_id: str
    spotify_track_id: str
    spotify_album_id: str


class UserListeningActivity(UserListeningActivityBase):
    id: int
    spotify_user_id: str
    spotify_track_id: str
    spotify_album_id: str

    class Config:
        from_attributes = True
