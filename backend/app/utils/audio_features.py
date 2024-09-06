from sqlalchemy.orm import Session
from models.audio_features import AudioFeature
from schemas.audio_features import AudioFeatureCreate
import requests
from config import SPOTIFY_API_BASE_URL


def get_audio_feature_by_track_id(db: Session, track_id: str) -> AudioFeature:
    return db.query(AudioFeature).filter(AudioFeature.id == track_id).first()


def create_or_update_audio_feature(db: Session, track_id: str, audio_feature: AudioFeatureCreate) -> AudioFeature:
    db_audio_feature = get_audio_feature_by_track_id(db, track_id)
    if db_audio_feature:
        for key, value in audio_feature.dict().items():
            if key != 'id':
                setattr(db_audio_feature, key, value)
    else:
        db_audio_feature = AudioFeature(
            id=track_id,
            **{key: value for key, value in audio_feature.dict().items() if key != 'id'}
        )
        db.add(db_audio_feature)
    db.commit()
    db.refresh(db_audio_feature)
    return db_audio_feature


def fetch_audio_features_from_spotify(track_spotify_id: str, access_token: str) -> AudioFeatureCreate:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/audio-features/{track_spotify_id}", headers=headers)

    if response.status_code == 200:
        new_audio_feature = response.json()
        updated_audio_feature = AudioFeatureCreate(
            id=track_spotify_id,
            danceability=new_audio_feature["danceability"],
            energy=new_audio_feature["energy"],
            key=new_audio_feature["key"],
            loudness=new_audio_feature["loudness"],
            mode=new_audio_feature["mode"],
            speechiness=new_audio_feature["speechiness"],
            acousticness=new_audio_feature["acousticness"],
            instrumentalness=new_audio_feature["instrumentalness"],
            liveness=new_audio_feature["liveness"],
            valence=new_audio_feature["valence"],
            tempo=new_audio_feature["tempo"],
            time_signature=new_audio_feature["time_signature"]
        )
    else:
        raise Exception(f"""Failed to fetch audio features from Spotify: {
                        response.status_code}""")

    return updated_audio_feature
