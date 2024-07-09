from sqlalchemy.orm import Session
from models.spotify_tokens import SpotifyToken
from schemas.spotify_tokens import SpotifyTokenCreate
from datetime import datetime, timedelta
import requests
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import logging

# Define a buffer time (e.g., 30 minutes) to refresh the token before it expires
REFRESH_BUFFER = timedelta(minutes=30)


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


def refresh_spotify_token(db: Session, user_id: int):
    spotify_token = get_spotify_token(db, user_id)
    if not spotify_token:
        logging.warning(f"No token found for user {user_id}")
        return None

    # Check if the token will expire within the buffer time
    if datetime.utcnow() + REFRESH_BUFFER < spotify_token.expires_at:
        logging.info(f"Token for user {
                     user_id} is still valid and not close to expiration")
        return spotify_token

    # Token is expired or will expire soon, refresh it
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
        expires_at=datetime.utcnow() +
        timedelta(seconds=new_token_info['expires_in']),
        refresh_token=new_token_info.get(
            'refresh_token', spotify_token.refresh_token),
        scope=new_token_info.get('scope', spotify_token.scope)
    )

    updated_token = create_or_update_spotify_token(db, user_id, token_update)
    logging.info(f"Successfully refreshed token for user {user_id}")
    return updated_token
