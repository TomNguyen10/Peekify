from sqlalchemy import Column, Integer, String, DateTime
from data.postgresql import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    spotify_user_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    profile_url = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(),
                        onupdate=datetime.now())
