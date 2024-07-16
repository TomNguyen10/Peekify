from sqlalchemy.orm import Session
from models.user_listening_activity import UserListeningActivity
from schemas.user_listening_activity import UserListeningActivityCreate
from typing import List
import requests
from datetime import datetime
from config import SPOTIFY_API_BASE_URL
from .track import get_or_create_track


def fetch_and_store_recent_user_activity(db: Session, user_spotify_id: str, access_token: str) -> List[UserListeningActivity]:
    recently_played = fetch_recently_played_tracks(access_token)

    new_activities = []

    for item in recently_played:
        track_data = item['track']
        played_at = datetime.fromisoformat(item['played_at'].rstrip('Z'))

        # Check if this activity already exists
        existing_activity = db.query(UserListeningActivity).filter(
            UserListeningActivity.user_spotify_id == user_spotify_id,
            UserListeningActivity.track_spotify_id == track_data['id'],
            UserListeningActivity.activity_listened_at == played_at
        ).first()

        if existing_activity:
            continue  # Skip if activity already exists

        # Get or create track (this will also handle album and artist creation)
        track = get_or_create_track(db, track_data['id'], access_token)

        # Create new activity
        new_activity = UserListeningActivity(**UserListeningActivityCreate(
            user_spotify_id=user_spotify_id,
            track_spotify_id=track.track_spotify_id,
            album_spotify_id=track.track_album_spotify_id,
            activity_listened_at=played_at
        ).model_dump())

        db.add(new_activity)
        new_activities.append(new_activity)

    db.commit()
    return new_activities


def fetch_recently_played_tracks(access_token: str, limit: int = 50) -> List[dict]:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"limit": limit}
    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/me/player/recently-played", headers=headers, params=params)

    if response.status_code == 200:
        return response.json()['items']
    else:
        raise Exception(f"Failed to fetch recently played tracks from Spotify: {
                        response.status_code}")
