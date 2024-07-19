from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from data.postgresql import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    country = Column(String)
    images = Column(String)
    profile_url = Column(String)
    created_at = Column(DateTime, default=datetime.now())

    spotify_token = relationship(
        "SpotifyToken", back_populates="user", uselist=False)
    listening_activities = relationship(
        "UserListeningActivity", back_populates="user")
