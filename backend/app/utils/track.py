from sqlalchemy.orm import Session
from models.track import Track
from schemas.track import TrackCreate
import requests
from config import SPOTIFY_API_BASE_URL


def get_track_by_spotify_id(db: Session, spotify_track_id: str) -> Track:
    return db.query(Track).filter(Track.id == spotify_track_id).first()


def create_or_update_track(db: Session, spotify_track_id: str, track: TrackCreate) -> Track:
    db_track = get_track_by_spotify_id(db, spotify_track_id)
    if db_track:
        for key, value in track.dict().items():
            if key != 'id':
                setattr(db_track, key, value)
    else:
        db_track = Track(
            id=spotify_track_id,
            **{key: value for key, value in track.dict().items() if key != 'id'}
        )
        db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track


def fetch_track_from_spotify(track_spotify_id: str, access_token: str) -> TrackCreate:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/tracks/{track_spotify_id}", headers=headers)

    if response.status_code == 200:
        new_track = response.json()
        updated_track = TrackCreate(
            id=new_track["id"],
            name=new_track["name"],
            href=new_track["href"],
            duration_ms=new_track["duration_ms"],
            popularity=new_track["popularity"],
            uri=new_track["uri"],
            album_spotify_id=new_track["album"]["id"],
            artist_spotify_ids=[artist["id"]
                                for artist in new_track["artists"]]
        )
    else:
        raise Exception(f"Failed to fetch track from Spotify: {
                        response.status_code}")

    return updated_track
