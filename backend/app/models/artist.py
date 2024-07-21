from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from data.postgresql import Base


class Artist(Base):
    __tablename__ = "artists"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    href = Column(String)
    followers = Column(Integer)
    genres = Column(ARRAY(String))
    popularity = Column(Integer)
    uri = Column(String)
    images = Column(String)
