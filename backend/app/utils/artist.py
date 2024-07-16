from sqlalchemy.orm import Session
from models.artist import Artist
from schemas.artist import ArtistCreate
import requests
from config import SPOTIFY_API_BASE_URL


def get_or_create_artist(db: Session, artist_spotify_id: str, access_token: str) -> Artist:
    artist = db.query(Artist).filter(
        Artist.artist_spotify_id == artist_spotify_id).first()
    if not artist:
        artist_data = fetch_artist_from_spotify(
            artist_spotify_id, access_token)
        artist = Artist(**ArtistCreate(**artist_data).model_dump())
        db.add(artist)
        db.flush()
    return artist


def fetch_artist_from_spotify(artist_spotify_id: str, access_token: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/artists/{artist_spotify_id}", headers=headers)

    if response.status_code == 200:
        artist_data = response.json()
        return {
            "artist_spotify_id": artist_data["id"],
            "artist_name": artist_data["name"],
            "artist_href": artist_data["href"],
            "artist_followers": artist_data["followers"]["total"],
            "artist_genres": artist_data["genres"],
            "artist_popularity": artist_data["popularity"],
            "artist_uri": artist_data["uri"],
            "artist_images": [image["url"] for image in artist_data["images"]]
        }
    else:
        raise Exception(f"Failed to fetch artist from Spotify: {
                        response.status_code}")
