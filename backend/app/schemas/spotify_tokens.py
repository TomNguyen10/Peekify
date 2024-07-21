from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SpotifyTokenBase(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_at: datetime
    scope: Optional[str] = None


class SpotifyTokenCreate(SpotifyTokenBase):
    pass


class SpotifyToken(SpotifyTokenBase):
    id: int
    user_id: str

    class Config:
        from_attributes = True
