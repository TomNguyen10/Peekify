from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from data.postgresql import Base


class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column(Integer, primary_key=True, index=True)
    spotify_artist_id = Column(String, unique=True, index=True)
    name = Column(String)
    href = Column(String)
    followers = Column(Integer)
    genres = Column(ARRAY(String))
    popularity = Column(Integer)
    uri = Column(String)
    images = Column(String)
