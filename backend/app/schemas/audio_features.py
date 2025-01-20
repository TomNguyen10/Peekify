# Remove since Spotify API stop providing audio features for tracks

from pydantic import BaseModel


class AudioFeatureBase(BaseModel):
    id: str
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    time_signature: int


class AudioFeatureCreate(AudioFeatureBase):
    pass


class AudioFeature(AudioFeatureBase):
    class Config:
        from_attributes = True
