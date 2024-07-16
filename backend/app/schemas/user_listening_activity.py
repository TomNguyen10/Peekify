from pydantic import BaseModel
from datetime import datetime


class UserListeningActivityBase(BaseModel):
    activity_listened_at: datetime


class UserListeningActivityCreate(UserListeningActivityBase):
    pass


class UserListeningActivity(UserListeningActivityBase):
    activity_id: int
    user_spotify_id: str
    track_spotify_id: str
    album_spotify_id: str

    class Config:
        from_attributes = True
