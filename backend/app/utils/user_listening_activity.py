from sqlalchemy import func, any_, and_, String
from sqlalchemy.orm import Session, aliased
from models.user_listening_activity import UserListeningActivity
from schemas.user_listening_activity import UserListeningActivityCreate
from typing import List
import requests
from datetime import datetime, timezone
from models.track import Track
from models.album import Album
from models.artist import Artist
from models.audio_features import AudioFeature
from utils.album import fetch_album_from_spotify, create_or_update_album
from utils.artist import fetch_artist_from_spotify, create_or_update_artist
from utils.track import fetch_track_from_spotify, create_or_update_track
from utils.audio_features import fetch_audio_features_from_spotify, create_or_update_audio_feature
from config import SPOTIFY_API_BASE_URL
from utils.time import get_date_range_for_last_week
import logging
import pandas as pd


def get_activity_by_ids(db: Session, spotify_user_id: str, spotify_track_id: str, activity_listened_at: datetime) -> UserListeningActivity:
    return db.query(UserListeningActivity).filter(
        UserListeningActivity.spotify_user_id == spotify_user_id,
        UserListeningActivity.spotify_track_id == spotify_track_id,
        UserListeningActivity.activity_listened_at == activity_listened_at
    ).first()


def parse_spotify_timestamp(timestamp_str: str) -> datetime:
    try:
        # Try parsing with microseconds, making it timezone-aware
        return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
    except ValueError:
        # Fallback to parsing without microseconds, also making it timezone-aware
        return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S%z')


def fetch_and_store_recent_user_activity(db: Session, user_spotify_id: int, access_token: str) -> List[UserListeningActivity]:
    recently_played = fetch_recently_played_tracks(access_token)

    # Sort activities by played_at time
    recently_played.sort(key=lambda x: x['played_at'])

    # Minimum play duration threshold in milliseconds (30 seconds)
    min_play_duration_ms = 30000
    min_play_duration_percentage = 0.3

    new_activities = []

    for i in range(len(recently_played) - 1):
        item = recently_played[i]
        next_item = recently_played[i + 1]
        track = item['track']
        track_id = track['id']
        album = track['album']
        album_id = album['id']
        artists = track['artists']
        played_at_str = item['played_at']
        logging.debug(f"Processing track {track_id} played at {played_at_str}")
        played_at = datetime.fromisoformat(played_at_str.rstrip('Z'))
        # Convert played_at times to datetime objects
        current_played_at = parse_spotify_timestamp(item['played_at'])
        next_played_at = parse_spotify_timestamp(next_item['played_at'])

        # Calculate duration between consecutive tracks in milliseconds
        listened_duration_ms = (
            next_played_at - current_played_at).total_seconds() * 1000

        if listened_duration_ms >= min_play_duration_ms or listened_duration_ms >= min_play_duration_percentage * track['duration_ms']:

            album_data = fetch_album_from_spotify(album_id, access_token)
            create_or_update_album(db, album_id, album_data)

            for artist in artists:
                artist_data = fetch_artist_from_spotify(
                    artist['id'], access_token)
                create_or_update_artist(db, artist['id'], artist_data)

            track_data = fetch_track_from_spotify(track_id, access_token)
            create_or_update_track(db, track_id, track_data)

            audio_feature_data = fetch_audio_features_from_spotify(
                track_id, access_token)
            create_or_update_audio_feature(db, track_id, audio_feature_data)

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
        logging.error(f"""Failed to fetch recently played tracks from Spotify: {
                      response.status_code} {response.text}""")
        response.raise_for_status()


def get_last_week_listening_activities(db: Session, user_spotify_id: str):
    last_monday, last_sunday = get_date_range_for_last_week()

    ArtistAlias = aliased(Artist)

    activities = (db.query(
        UserListeningActivity.activity_listened_at,
        Track.name.label('track_name'),
        Track.duration_ms.label('track_duration'),
        Track.popularity.label('track_popularity'),
        Album.name.label('album_name'),
        Album.release_date.label('album_release_date'),
        Album.total_tracks.label('album_total_tracks'),
        Album.genres.label('album_genres'),
        func.string_agg(ArtistAlias.name, ', ').label('artist_names'),
        func.string_agg(ArtistAlias.genres[1], ', ').label('artist_genres'),
        func.string_agg(func.cast(ArtistAlias.popularity, String),
                        ', ').label('artist_popularity'),
        AudioFeature.danceability,
        AudioFeature.energy,
        AudioFeature.key,
        AudioFeature.loudness,
        AudioFeature.mode,
        AudioFeature.speechiness,
        AudioFeature.acousticness,
        AudioFeature.instrumentalness,
        AudioFeature.liveness,
        AudioFeature.valence,
        AudioFeature.tempo
    )
        .join(Track, UserListeningActivity.spotify_track_id == Track.id)
        .join(Album, Track.album_spotify_id == Album.id)
        .join(AudioFeature, Track.id == AudioFeature.id)
        .join(ArtistAlias, ArtistAlias.id == any_(Track.artist_spotify_ids))
        .filter(UserListeningActivity.spotify_user_id == user_spotify_id)
        .filter(and_(
            UserListeningActivity.activity_listened_at >= last_monday,
            UserListeningActivity.activity_listened_at <= last_sunday
        ))
        .group_by(
        UserListeningActivity.activity_listened_at,
        Track.name, Track.duration_ms, Track.popularity,
        Album.name, Album.release_date, Album.total_tracks, Album.genres,
        AudioFeature.danceability, AudioFeature.energy, AudioFeature.key,
        AudioFeature.loudness, AudioFeature.mode, AudioFeature.speechiness,
        AudioFeature.acousticness, AudioFeature.instrumentalness,
        AudioFeature.liveness, AudioFeature.valence, AudioFeature.tempo
    )
        .order_by(UserListeningActivity.activity_listened_at)
        .all())

    # Unpacking query results properly
    data = [{
        "activity_listened_at": activity_listened_at,
        "track_name": track_name,
        "track_duration": track_duration,
        "track_popularity": track_popularity,
        "album_name": album_name,
        "album_release_date": album_release_date,
        "album_total_tracks": album_total_tracks,
        "album_genres": album_genres,
        "artist_names": artist_names,
        "artist_genres": artist_genres,
        "artist_popularity": artist_popularity,
        "danceability": danceability,
        "energy": energy,
        "key": key,
        "loudness": loudness,
        "mode": mode,
        "speechiness": speechiness,
        "acousticness": acousticness,
        "instrumentalness": instrumentalness,
        "liveness": liveness,
        "valence": valence,
        "tempo": tempo
    } for activity_listened_at, track_name, track_duration, track_popularity, album_name, album_release_date, album_total_tracks, album_genres,
        artist_names, artist_genres, artist_popularity, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo in activities]

    # Create DataFrame for manipulation
    df = pd.DataFrame(data)
    return df
