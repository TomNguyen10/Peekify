from pydantic import BaseModel
from typing import List


class ArtistBase(BaseModel):
    id: str
    name: str
    href: str
    followers: int
    genres: List[str]
    popularity: int
    uri: str
    images: str


class ArtistCreate(ArtistBase):
    pass


class Artist(ArtistBase):
    class Config:
        from_attributes = True
