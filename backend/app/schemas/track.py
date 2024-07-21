from pydantic import BaseModel
from typing import List


class TrackBase(BaseModel):
    id: str
    name: str
    href: str
    duration_ms: int
    popularity: int
    uri: str
    album_spotify_id: str
    artist_spotify_ids: List[str]


class TrackCreate(TrackBase):
    pass


class Track(TrackBase):
    class Config:
        from_attributes = True
