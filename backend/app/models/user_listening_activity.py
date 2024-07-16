from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from data.postgresql import Base


class UserListeningActivity(Base):
    __tablename__ = "user_listening_activities"

    activity_id = Column(Integer, primary_key=True, index=True)
    spotify_user_id = Column(String, ForeignKey("users.spotify_user_id"))
    spotify_track_id = Column(String, ForeignKey("tracks.spotify_track_id"))
    spotify_album_id = Column(String, ForeignKey("albums.spotify_album_id"))
    activity_listened_at = Column(DateTime)

    user = relationship("User", back_populates="listening_activities")
    track = relationship("Track", back_populates="listening_activities")
    album = relationship("Album", back_populates="listening_activities")
