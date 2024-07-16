from sqlalchemy.orm import Session
from models.album import Album
from schemas.album import AlbumCreate
import requests
from config import SPOTIFY_API_BASE_URL


def get_or_create_album(db: Session, album_spotify_id: str, access_token: str) -> Album:
    album = db.query(Album).filter(
        Album.album_spotify_id == album_spotify_id).first()
    if not album:
        album_data = fetch_album_from_spotify(album_spotify_id, access_token)
        album = Album(**AlbumCreate(**album_data).model_dump())
        db.add(album)
        db.flush()
    return album


def fetch_album_from_spotify(album_spotify_id: str, access_token: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/albums/{album_spotify_id}", headers=headers)

    if response.status_code == 200:
        album_data = response.json()
        return {
            "album_spotify_id": album_data["id"],
            "album_name": album_data["name"],
            "album_href": album_data["href"],
            "album_release_date": album_data["release_date"],
            "album_total_tracks": album_data["total_tracks"],
            "album_type": album_data["album_type"],
            "album_genres": album_data["genres"],
            "album_popularity": album_data["popularity"],
            "album_uri": album_data["uri"],
            "album_images": [image["url"] for image in album_data["images"]],
            "album_artist_spotify_ids": [artist["id"] for artist in album_data["artists"]]
        }
    else:
        raise Exception(f"Failed to fetch album from Spotify: {
                        response.status_code}")
