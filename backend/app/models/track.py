from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from data.postgresql import Base


class Track(Base):
    __tablename__ = "tracks"

    track_id = Column(Integer, primary_key=True, index=True)
    spotify_track_id = Column(String, unique=True, index=True)
    name = Column(String)
    href = Column(String)
    duration_ms = Column(Integer)
    popularity = Column(Integer)
    genres = Column(ARRAY(String))
    uri = Column(String)
    spotify_album_id = Column(
        String, ForeignKey("albums.spotify_album_id"))
    artist_spotify_ids = Column(ARRAY(String))

    album = relationship(
        "Album", back_populates="tracks")
    listening_activities = relationship(
        "UserListeningActivity", back_populates="track")
