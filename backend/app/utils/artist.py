from sqlalchemy.orm import Session
from models.artist import Artist
from schemas.artist import ArtistCreate
import requests
from config import SPOTIFY_API_BASE_URL


def get_artist_by_spotify_id(db: Session, spotify_artist_id: str) -> Artist:
    # Changed to 'id'
    return db.query(Artist).filter(Artist.id == spotify_artist_id).first()


def create_or_update_artist(db: Session, spotify_artist_id: str, artist: ArtistCreate) -> Artist:
    db_artist = get_artist_by_spotify_id(db, spotify_artist_id)
    if db_artist:
        for key, value in artist.dict().items():
            if key != 'id':
                setattr(db_artist, key, value)
    else:
        db_artist = Artist(
            id=spotify_artist_id,
            **{key: value for key, value in artist.dict().items() if key != 'id'}
        )
        db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist


def fetch_artist_from_spotify(artist_spotify_id: str, access_token: str) -> ArtistCreate:
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}/artists/{artist_spotify_id}", headers=headers)

    if response.status_code == 200:
        new_artist = response.json()
        updated_artist = ArtistCreate(
            id=new_artist["id"],
            name=new_artist["name"],
            href=new_artist["href"],
            followers=new_artist["followers"]["total"],
            genres=new_artist["genres"],
            popularity=new_artist["popularity"],
            uri=new_artist["uri"],
            images=str(new_artist.get('images')),
        )
    else:
        raise Exception(f"""Failed to fetch artist from Spotify: {
                        response.status_code}""")

    return updated_artist


def get_artist_names(db: Session, artist_ids):
    artist_names = db.query(Artist.name).filter(
        Artist.id.in_(artist_ids)).all()
    return [artist.name for artist in artist_names]
