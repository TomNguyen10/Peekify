from sqlalchemy.orm import Session
from models.user import User
from models.spotify_tokens import SpotifyToken
from schemas.user import UserCreate
from schemas.spotify_tokens import SpotifyTokenCreate
from datetime import datetime, timedelta
import requests
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import logging

# Define a buffer time (e.g., 15 minutes) to refresh the token before it expires
REFRESH_BUFFER = timedelta(minutes=15)


def get_spotify_token(db: Session, user_id: int) -> SpotifyToken:
    return db.query(SpotifyToken).filter(SpotifyToken.user_id == user_id).first()


def create_or_update_spotify_token(db: Session, user_id: str, token: SpotifyTokenCreate):
    db_token = db.query(SpotifyToken).filter(
        SpotifyToken.user_id == user_id).first()
    if db_token:
        db_token.access_token = token.access_token
        db_token.refresh_token = token.refresh_token
        db_token.token_type = token.token_type
        db_token.expires_at = token.expires_at
        db_token.scope = token.scope
    else:
        db_token = SpotifyToken(user_id=user_id, **token.dict())
        db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def refresh_spotify_token(db: Session, user_id: str):
    spotify_token = get_spotify_token(db, user_id)
    if not spotify_token:
        logging.warning(f"No token found for user {user_id}")
        return None

    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": spotify_token.refresh_token,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(token_url, data=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to refresh token for user {user_id}: {str(e)}")
        return None

    new_token_info = response.json()

    # Update token in database
    token_update = SpotifyTokenCreate(
        access_token=new_token_info['access_token'],
        token_type=new_token_info['token_type'],
        expires_at=datetime.now() +
        timedelta(seconds=new_token_info['expires_in']),
        refresh_token=new_token_info.get(
            'refresh_token', spotify_token.refresh_token),
        scope=new_token_info.get('scope', spotify_token.scope)
    )

    updated_token = create_or_update_spotify_token(db, user_id, token_update)
    logging.info(f"Successfully refreshed token for user {user_id}")
    return updated_token
