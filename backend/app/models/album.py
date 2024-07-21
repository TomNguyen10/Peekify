from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from data.postgresql import Base


class Album(Base):
    __tablename__ = "albums"

    id = Column(String, primary_key=True, index=True)
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
    tracks = relationship("Track", back_populates="album")
    listening_activities = relationship(
        "UserListeningActivity", back_populates="album")
