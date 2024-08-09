from sqlalchemy.orm import Session
from models.album import Album
from schemas.album import AlbumCreate
import requests
from config import SPOTIFY_API_BASE_URL


def get_album_by_spotify_id(db: Session, spotify_album_id: str) -> Album:
    return db.query(Album).filter(Album.id == spotify_album_id).first()


def create_or_update_album(db: Session, spotify_album_id: str, album: AlbumCreate) -> Album:
    db_album = get_album_by_spotify_id(db, spotify_album_id)
    if db_album:
        for key, value in album.dict().items():
            if key != 'id':
                setattr(db_album, key, value)
    else:
        db_album = Album(
            id=spotify_album_id,
            **{key: value for key, value in album.dict().items() if key != 'id'}
        )
        db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album


def fetch_album_from_spotify(album_spotify_id: str, access_token: str) -> AlbumCreate:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/albums/{album_spotify_id}", headers=headers)

    if response.status_code == 200:
        new_album = response.json()
        updated_album = AlbumCreate(
            id=new_album["id"],
            name=new_album["name"],
            href=new_album["href"],
            release_date=new_album["release_date"],
            total_tracks=new_album["total_tracks"],
            album_type=new_album["album_type"],
            genres=new_album["genres"],
            label=new_album.get("label", None),
            popularity=new_album["popularity"],
            uri=new_album["uri"],
            images=str(new_album.get('images')),
            artist_spotify_ids=[artist["id"]
                                for artist in new_album["artists"]]
        )
    else:
        raise Exception(f"""Failed to fetch album from Spotify: {
                        response.status_code}""")

    return updated_album
