from sqlalchemy.orm import Session
from models.user_listening_activity import UserListeningActivity
from schemas.user_listening_activity import UserListeningActivityCreate
from typing import List
import requests
from datetime import datetime
from utils.album import fetch_album_from_spotify, get_album_by_spotify_id, create_or_update_album
from utils.artist import fetch_artist_from_spotify, get_artist_by_spotify_id, create_or_update_artist
from utils.track import fetch_track_from_spotify, get_track_by_spotify_id, create_or_update_track
from config import SPOTIFY_API_BASE_URL
import logging


def get_activity_by_ids(db: Session, spotify_user_id: str, spotify_track_id: str, activity_listened_at: datetime) -> UserListeningActivity:
    return db.query(UserListeningActivity).filter(
        UserListeningActivity.spotify_user_id == spotify_user_id,
        UserListeningActivity.spotify_track_id == spotify_track_id,
        UserListeningActivity.activity_listened_at == activity_listened_at
    ).first()


def fetch_and_store_recent_user_activity(db: Session, user_spotify_id: int, access_token: str) -> List[UserListeningActivity]:
    recently_played = fetch_recently_played_tracks(access_token)

    new_activities = []

    for item in recently_played:
        track = item['track']
        track_id = track['id']
        album = track['album']
        album_id = album['id']
        artists = track['artists']
        played_at_str = item['played_at']
        played_at = datetime.fromisoformat(played_at_str.rstrip('Z'))

        existing_album = get_album_by_spotify_id(db, album_id)
        if not existing_album:
            album_data = fetch_album_from_spotify(album_id, access_token)
            create_or_update_album(db, album_id, album_data)

        for artist in artists:
            existing_artist = get_artist_by_spotify_id(db, artist['id'])
            if not existing_artist:
                artist_data = fetch_artist_from_spotify(
                    artist['id'], access_token)
                create_or_update_artist(db, artist['id'], artist_data)

        existing_track = get_track_by_spotify_id(db, track_id)
        if not existing_track:
            track_data = fetch_track_from_spotify(track_id, access_token)
            create_or_update_track(db, track_id, track_data)

        existing_activity = get_activity_by_ids(
            db, user_spotify_id, track_id, played_at)
        if existing_activity:
            continue

        new_activity_data = UserListeningActivityCreate(
            spotify_user_id=user_spotify_id,
            spotify_track_id=track_id,
            spotify_album_id=album_id,
            activity_listened_at=played_at
        )

        logging.debug(f"Creating new UserListeningActivity with spotify_user_id: {user_spotify_id}, "
                      f"spotify_track_id: {track_id}, spotify_album_id: {album_id}, activity_listened_at: {played_at}")

        new_activity = UserListeningActivity(**new_activity_data.dict())
        db.add(new_activity)
        new_activities.append(new_activity)

    # Commit and refresh outside the loop for performance
    if new_activities:
        db.commit()
        for new_activity in new_activities:
            db.refresh(new_activity)

    return new_activities


def fetch_recently_played_tracks(access_token: str, limit: int = 50) -> List[dict]:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"limit": limit}
    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/me/player/recently-played", headers=headers, params=params)

    if response.status_code == 200:
        return response.json()['items']
    else:
        logging.error(f"Failed to fetch recently played tracks from Spotify: {
                      response.status_code} {response.text}")
        response.raise_for_status()
