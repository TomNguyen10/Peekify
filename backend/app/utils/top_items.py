from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import datetime
from models.user_listening_activity import UserListeningActivity
from models.track import Track
from models.artist import Artist
from models.album import Album


def get_top_5_tracks_last_week(db: Session, user_spotify_id: str):
    # Get the current time and calculate the start and end of last week
    today = datetime.datetime.now()

    # Calculate the previous Monday by going back to the most recent Monday
    last_monday = today - timedelta(days=today.weekday(), weeks=1)

    # Set the time to 00:00:00 for last Monday
    last_monday = last_monday.replace(
        hour=0, minute=0, second=0, microsecond=0)

    # Calculate the last Sunday (23:59:59 of that week)
    last_sunday = last_monday + \
        timedelta(days=6, hours=23, minutes=59, seconds=59)

    # Query the UserListeningActivity table to filter activities in the last week
    # and count occurrences of each track
    top_tracks_query = (db.query(
        UserListeningActivity.spotify_track_id,
        func.count(UserListeningActivity.spotify_track_id).label('track_count'))
        .filter(UserListeningActivity.spotify_user_id == user_spotify_id)
        .filter(UserListeningActivity.activity_listened_at >= last_monday)
        .filter(UserListeningActivity.activity_listened_at <= last_sunday)
        .group_by(UserListeningActivity.spotify_track_id)
        .order_by(desc('track_count'))
        .limit(5)
        .all())

    # Get detailed track info by joining with the Track table
    top_tracks = []
    for track_id, count in top_tracks_query:
        # Fetch the track details
        track = db.query(Track).filter(Track.id == track_id).first()

        # Fetch the artist(s) for the track
        artist_names = (
            db.query(Artist.name)
            .filter(Artist.id.in_(track.artist_spotify_ids))
            .all()
        )
        artist_names = [artist.name for artist in artist_names]

        # Fetch the album for the track
        album = db.query(Album).filter(Album.id ==
                                       track.album_spotify_id).first()

        top_tracks.append({
            "track_id": track_id,
            "track_name": track.name,
            "artist_name": ", ".join(artist_names),
            "album_name": album.name if album else "Unknown Album",
            "play_count": count,
        })

    return top_tracks


def get_top_5_artists_last_week(db: Session, user_spotify_id: str):
    # Get the current time and calculate the start and end of last week
    today = datetime.datetime.now()

    # Calculate the previous Monday by going back to the most recent Monday
    last_monday = today - timedelta(days=today.weekday(), weeks=1)

    # Set the time to 00:00:00 for last Monday
    last_monday = last_monday.replace(
        hour=0, minute=0, second=0, microsecond=0)

    # Calculate the last Sunday (23:59:59 of that week)
    last_sunday = last_monday + \
        timedelta(days=6, hours=23, minutes=59, seconds=59)

    # Query the UserListeningActivity table to filter activities in the last week
    # and count occurrences of each artist based on the tracks played
    top_artists_query = (
        db.query(Track.artist_spotify_ids, func.count(
            Track.artist_spotify_ids).label("artist_count"))
        .join(UserListeningActivity, UserListeningActivity.spotify_track_id == Track.id)
        .filter(UserListeningActivity.spotify_user_id == user_spotify_id)
        .filter(UserListeningActivity.activity_listened_at >= last_monday)
        .filter(UserListeningActivity.activity_listened_at <= last_sunday)
        .group_by(Track.artist_spotify_ids)
        .order_by(desc("artist_count"))
        .limit(5)
        .all()
    )

    # Get detailed artist info by querying the Artist table
    top_artists = []
    for artist_ids, count in top_artists_query:
        # Fetch artist details (assuming `artist_spotify_ids` is a list of Spotify IDs)
        artist_names = (
            db.query(Artist.name)
            # Handling multiple artists for a track
            .filter(Artist.id.in_(artist_ids))
            .all()
        )
        artist_names = [artist.name for artist in artist_names]

        top_artists.append({
            # Join multiple artist names
            "artist_name": ", ".join(artist_names),
            "play_count": count
        })

    return top_artists


# Helper function to calculate start of the most recent Monday
def get_most_recent_monday():
    today = datetime.datetime.now()
    # Move to the most recent Monday
    monday = today - timedelta(days=today.weekday())
    return monday.replace(hour=0, minute=0, second=0, microsecond=0)


def get_songs_per_day(db: Session, user_spotify_id: str):
    monday = get_most_recent_monday()

    # Group the listening activity by day
    songs_per_day = (
        db.query(func.date(UserListeningActivity.activity_listened_at),
                 func.count(UserListeningActivity.spotify_track_id))
        .filter(UserListeningActivity.spotify_user_id == user_spotify_id)
        .filter(UserListeningActivity.activity_listened_at >= monday)
        .group_by(func.date(UserListeningActivity.activity_listened_at))
        .order_by(func.date(UserListeningActivity.activity_listened_at))
        .all()
    )

    return [{"date": date, "song_count": count} for date, count in songs_per_day]


def get_top_songs_this_week(db: Session, user_spotify_id: str, limit=5):
    monday = get_most_recent_monday()
    today = datetime.datetime.now()

    # Query for the top songs this week
    top_songs_query = (
        db.query(
            UserListeningActivity.spotify_track_id,
            func.count(UserListeningActivity.spotify_track_id).label(
                'track_count')
        )
        .filter(UserListeningActivity.spotify_user_id == user_spotify_id)
        .filter(UserListeningActivity.activity_listened_at >= monday)
        .filter(UserListeningActivity.activity_listened_at <= today)
        .group_by(UserListeningActivity.spotify_track_id)
        .order_by(desc('track_count'))
        .limit(limit)
        .all()
    )

    top_songs = []
    for track_id, count in top_songs_query:
        track = db.query(Track).filter(Track.id == track_id).first()
        artist_names = (
            db.query(Artist.name)
            .filter(Artist.id.in_(track.artist_spotify_ids))
            .all()
        )
        artist_names = [artist.name for artist in artist_names]

        top_songs.append({
            "track_name": track.name,
            "artist_name": ", ".join(artist_names),
            "play_count": count,
        })

    return top_songs


def get_top_artists_this_week(db: Session, user_spotify_id: str, limit=5):
    monday = get_most_recent_monday()
    today = datetime.datetime.now()

    # Query for the top artists this week
    top_artists_query = (
        db.query(Track.artist_spotify_ids, func.count(
            Track.artist_spotify_ids).label("artist_count"))
        .join(UserListeningActivity, UserListeningActivity.spotify_track_id == Track.id)
        .filter(UserListeningActivity.spotify_user_id == user_spotify_id)
        .filter(UserListeningActivity.activity_listened_at >= monday)
        .filter(UserListeningActivity.activity_listened_at <= today)
        .group_by(Track.artist_spotify_ids)
        .order_by(desc("artist_count"))
        .limit(limit)
        .all()
    )

    top_artists = []
    for artist_ids, count in top_artists_query:
        artist_names = (
            db.query(Artist.name)
            .filter(Artist.id.in_(artist_ids))
            .all()
        )
        artist_names = [artist.name for artist in artist_names]

        top_artists.append({
            "artist_name": ", ".join(artist_names),
            "play_count": count,
        })

    return top_artists
