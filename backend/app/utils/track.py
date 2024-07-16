from sqlalchemy.orm import Session
from models.track import Track
from schemas.track import TrackCreate
import requests
from config import SPOTIFY_API_BASE_URL
from .album import get_or_create_album
from .artist import get_or_create_artist


def get_or_create_track(db: Session, track_spotify_id: str, access_token: str) -> Track:
    track = db.query(Track).filter(
        Track.track_spotify_id == track_spotify_id).first()
    if not track:
        track_data = fetch_track_from_spotify(track_spotify_id, access_token)

        # Get or create album
        album = get_or_create_album(
            db, track_data['track_album_spotify_id'], access_token)

        # Get or create artists
        for artist_id in track_data['track_artist_spotify_ids']:
            get_or_create_artist(db, artist_id, access_token)

        track = Track(**TrackCreate(**track_data).model_dump())
        db.add(track)
        db.flush()
    return track


def fetch_track_from_spotify(track_spotify_id: str, access_token: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/tracks/{track_spotify_id}", headers=headers)

    if response.status_code == 200:
        track_data = response.json()
        return {
            "track_spotify_id": track_data["id"],
            "track_name": track_data["name"],
            "track_href": track_data["href"],
            "track_duration_ms": track_data["duration_ms"],
            "track_popularity": track_data["popularity"],
            "track_uri": track_data["uri"],
            "track_album_spotify_id": track_data["album"]["id"],
            "track_artist_spotify_ids": [artist["id"] for artist in track_data["artists"]]
        }
    else:
        raise Exception(f"Failed to fetch track from Spotify: {
                        response.status_code}")
