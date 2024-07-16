from pydantic import BaseModel
from typing import List


class AlbumBase(BaseModel):
    spotify_album_id: str
    name: str
    href: str
    release_date: str
    total_tracks: int
    album_type: str
    genres: List[str]
    label: str
    popularity: int
    uri: str
    images: List[str]
    artist_spotify_ids: List[str]


class AlbumCreate(AlbumBase):
    pass


class Album(AlbumBase):
    album_id: int

    class Config:
        from_attributes = True
