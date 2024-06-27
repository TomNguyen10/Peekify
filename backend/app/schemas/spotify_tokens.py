from pydantic import BaseModel
from datetime import datetime


class SpotifyTokenBase(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
    token_type: str
    expires_at: datetime
    scope: str


class SpotifyTokenCreate(SpotifyTokenBase):
    pass


class SpotifyToken(SpotifyTokenBase):
    token_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
