from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from data.postgresql import Base


class Album(Base):
    __tablename__ = "albums"

    album_id = Column(Integer, primary_key=True, index=True)
    spotify_album_id = Column(String, unique=True, index=True)
    name = Column(String)
    href = Column(String)
    release_date = Column(String)
    total_tracks = Column(Integer)
    album_type = Column(String)
    genres = Column(ARRAY(String))
    label = Column(String)
    popularity = Column(Integer)
    uri = Column(String)
    images = Column(String)
    artist_spotify_ids = Column(ARRAY(String))
    tracks = relationship(
        "Track", back_populates="album")
    listening_activities = relationship(
        "UserListeningActivity", back_populates="album")
