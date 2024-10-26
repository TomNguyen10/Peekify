from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from sqlalchemy.sql import text
from datetime import datetime
import calendar
import requests
import logging
from models.user_listening_activity import UserListeningActivity
from models.track import Track
from models.artist import Artist
from models.album import Album
from utils.artist import get_artist_names
from utils.time import get_date_range_for_last_week, get_most_recent_monday
from utils.image import parse_images, get_image_url


logger = logging.getLogger(__name__)


def get_top_items(db: Session, user_spotify_id: str, start_date, end_date, group_by, limit=5):
    return (db.query(group_by, func.count(group_by).label('count'))
            .select_from(UserListeningActivity)
            .join(Track, UserListeningActivity.spotify_track_id == Track.id)
            .filter(UserListeningActivity.spotify_user_id == user_spotify_id)
            .filter(UserListeningActivity.activity_listened_at >= start_date)
            .filter(UserListeningActivity.activity_listened_at <= end_date)
            .group_by(group_by)
            .order_by(desc('count'))
            .limit(limit)
            .all())


def get_top_5_tracks_last_week(db: Session, user_spotify_id: str):
    last_monday, last_sunday = get_date_range_for_last_week()
    top_tracks_query = get_top_items(
        db, user_spotify_id, last_monday, last_sunday, UserListeningActivity.spotify_track_id)

    top_tracks = []
    for track_id, count in top_tracks_query:
        track = db.query(Track).filter(Track.id == track_id).first()
        artist_names = get_artist_names(db, track.artist_spotify_ids)
        album = db.query(Album).filter(
            Album.id == track.album_spotify_id).first()

        top_tracks.append({
            "track_id": track_id,
            "track_name": track.name,
            "artist_name": ", ".join(artist_names),
            "album_name": album.name if album else "Unknown Album",
            "play_count": count,
        })

    return top_tracks


def get_top_5_artists_last_week(db: Session, user_spotify_id: str):
    last_monday, last_sunday = get_date_range_for_last_week()
    top_artists_query = get_top_items(
        db, user_spotify_id, last_monday, last_sunday, Track.artist_spotify_ids)

    top_artists = []
    for artist_ids, count in top_artists_query:
        artist_names = get_artist_names(db, artist_ids)
        top_artists.append({
            "artist_name": ", ".join(artist_names),
            "play_count": count
        })

    return top_artists


def get_songs_per_day(db: Session, user_spotify_id: str):
    monday = get_most_recent_monday()
    songs_per_day = (db.query(
        func.date(UserListeningActivity.activity_listened_at),
        func.count(UserListeningActivity.spotify_track_id),
        func.sum(Track.duration_ms))
        .join(Track, Track.id == UserListeningActivity.spotify_track_id)
        .filter(UserListeningActivity.spotify_user_id == user_spotify_id)
        .filter(UserListeningActivity.activity_listened_at >= monday)
        .group_by(func.date(UserListeningActivity.activity_listened_at))
        .order_by(func.date(UserListeningActivity.activity_listened_at))
        .all())

    return [{
        "date": date,
        "day": calendar.day_name[date.weekday()],
        "song_count": count,
        "total_duration_seconds": total_duration
    } for date, count, total_duration in songs_per_day]


def get_top_songs_this_week(db: Session, user_spotify_id: str, limit=5):
    monday = get_most_recent_monday()
    today = datetime.now()
    top_songs_query = get_top_items(
        db, user_spotify_id, monday, today, UserListeningActivity.spotify_track_id, limit)

    return [{
        "track_name": db.query(Track.name).filter(Track.id == track_id).first()[0],
        "artist_name": ", ".join(get_artist_names(db, db.query(Track.artist_spotify_ids).filter(Track.id == track_id).first()[0])),
        "play_count": count,
    } for track_id, count in top_songs_query]


def get_top_artists_this_week(db: Session, user_spotify_id: str, limit=5):
    try:
        monday = get_most_recent_monday()
        today = datetime.now()

        subquery = (db.query(Track.artist_spotify_ids, func.count(UserListeningActivity.id).label('play_count'))
                    .join(UserListeningActivity, UserListeningActivity.spotify_track_id == Track.id)
                    .filter(UserListeningActivity.spotify_user_id == user_spotify_id)
                    .filter(UserListeningActivity.activity_listened_at >= monday)
                    .filter(UserListeningActivity.activity_listened_at <= today)
                    .group_by(Track.artist_spotify_ids)
                    .subquery())

        top_artists_query = (db.query(Artist.id, Artist.name, Artist.images, func.sum(subquery.c.play_count).label('total_play_count'))
                             .filter(text(f"{subquery.c.artist_spotify_ids} @> ARRAY[artists.id]"))
                             .group_by(Artist.id, Artist.name, Artist.images)
                             .order_by(desc('total_play_count'))
                             .limit(limit)
                             .all())

        top_artists = []
        for artist in top_artists_query:
            images = parse_images(artist.images)
            top_artists.append({
                "artist_name": artist.name,
                "play_count": artist.total_play_count,
                "image_160x160": get_image_url(images, 160)
            })

        return top_artists

    except Exception as e:
        logger.error("Error fetching top artists this week: %s", e)
        raise

    except Exception as e:
        logger.error("Error fetching top artists this week: %s", e)
        raise


def get_top_albums_this_week(db: Session, user_spotify_id: str, limit=5):
    monday = get_most_recent_monday()
    today = datetime.now()
    top_albums_query = get_top_items(
        db, user_spotify_id, monday, today, Track.album_spotify_id, limit)

    return [{
        "name": album_record.name,
        "play_count": count,
        "album_image_64x64": get_image_url(parse_images(album_record.images), 64)
    } for album_id, count in top_albums_query
        for album_record in [db.query(Album.name, Album.images).filter(Album.id == album_id).first()]]


def get_user_top_items_from_spotify(access_token: str, item_type: str, time_range: str, limit: int = 20):
    top_items_url = f"https://api.spotify.com/v1/me/top/{item_type}"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"time_range": time_range, "limit": limit}
    response = requests.get(top_items_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        logging.error(f"""Failed to get top {item_type} for {time_range}: {
                      response.status_code} - {response.json()}""")
        return []
