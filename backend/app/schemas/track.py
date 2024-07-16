from pydantic import BaseModel
from typing import List


class TrackBase(BaseModel):
    spotify_track_id: str
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
    track_id: int
    album_spotify_id: str

    class Config:
        from_attributes = True
