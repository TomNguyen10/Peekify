from pydantic import BaseModel
from typing import List


class ArtistBase(BaseModel):
    spotify_artist_id: str
    name: str
    href: str
    followers: int
    genres: List[str]
    popularity: int
    uri: str
    images: List[str]


class ArtistCreate(ArtistBase):
    pass


class Artist(ArtistBase):
    artist_id: int

    class Config:
        from_attributes = True
