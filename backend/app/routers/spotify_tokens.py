from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data.postgresql import get_db
from models.spotify_tokens import SpotifyToken
from schemas.spotify_tokens import SpotifyTokenCreate, SpotifyToken as SpotifyTokenSchema

router = APIRouter()


def create_spotify_token(db: Session, token: SpotifyTokenCreate):
    db_token = SpotifyToken(**token.model_dump())
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


@router.post("/spotify/tokens/", response_model=SpotifyTokenSchema)
def create_spotify_token_endpoint(token: SpotifyTokenCreate, db: Session = Depends(get_db)):
    return create_spotify_token(db, token)
