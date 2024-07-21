from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from data.postgresql import Base


class UserListeningActivity(Base):
    __tablename__ = "user_listening_activities"

    id = Column(Integer, primary_key=True, index=True)
    spotify_user_id = Column(String, ForeignKey("users.id"))
    spotify_track_id = Column(String, ForeignKey("tracks.id"))
    spotify_album_id = Column(String, ForeignKey("albums.id"))
    activity_listened_at = Column(DateTime)

    user = relationship("User", back_populates="listening_activities")
    track = relationship("Track", back_populates="listening_activities")
    album = relationship("Album", back_populates="listening_activities")
