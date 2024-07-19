from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from data.postgresql import Base


class Track(Base):
    __tablename__ = "tracks"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    href = Column(String)
    duration_ms = Column(Integer)
    popularity = Column(Integer)
    genres = Column(ARRAY(String))
    uri = Column(String)
    album_spotify_id = Column(String, ForeignKey("albums.id"))
    artist_spotify_ids = Column(ARRAY(String))

    album = relationship("Album", back_populates="tracks")
    listening_activities = relationship(
        "UserListeningActivity", back_populates="track")
