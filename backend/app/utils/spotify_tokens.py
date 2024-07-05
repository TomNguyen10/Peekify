from sqlalchemy.orm import Session
from models.spotify_tokens import SpotifyToken
from schemas.spotify_tokens import SpotifyTokenCreate


def get_spotify_token(db: Session, user_id: int):
    return db.query(SpotifyToken).filter(SpotifyToken.user_id == user_id).first()


def create_or_update_spotify_token(db: Session, user_id: int, token: SpotifyTokenCreate):
    db_token = get_spotify_token(db, user_id)
    if db_token:
        for key, value in token.model_dump().items():
            setattr(db_token, key, value)
    else:
        db_token = SpotifyToken(**token.model_dump(), user_id=user_id)
        db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token
