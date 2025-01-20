# Remove since Spotify API stop providing audio features for tracks


from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from data.postgresql import Base


class AudioFeature(Base):
    __tablename__ = "audio_features"

    id = Column(String, ForeignKey("tracks.id"), primary_key=True, index=True)
    danceability = Column(Float)
    energy = Column(Float)
    key = Column(Integer)
    loudness = Column(Float)
    mode = Column(Integer)
    speechiness = Column(Float)
    acousticness = Column(Float)
    instrumentalness = Column(Float)
    liveness = Column(Float)
    valence = Column(Float)
    tempo = Column(Float)
    time_signature = Column(Integer)
