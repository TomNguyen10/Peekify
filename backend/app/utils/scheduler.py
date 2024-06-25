from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from data.postgresql import SessionLocal
from models.spotify_tokens import SpotifyToken
from models.user import User
from data.mongodb import insert_listening_activity
from datetime import datetime, timedelta
import requests
import os

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

scheduler = BackgroundScheduler()


def refresh_access_token(user_id: int, db: Session):
    token = db.query(SpotifyToken).filter(
        SpotifyToken.user_id == user_id).first()
    token_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(token_url, data={
        'grant_type': 'refresh_token',
        'refresh_token': token.refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    })

    if response.status_code == 200:
        token_info = response.json()
        token.access_token = token_info['access_token']
        token.expires_at = datetime.now(
        ) + timedelta(seconds=token_info['expires_in'])
        db.commit()
        return token.access_token
    else:
        raise Exception("Failed to refresh access token")


def fetch_and_store_listening_activities():
    db = SessionLocal()
    users = db.query(User).all()
    for user in users:
        token = db.query(SpotifyToken).filter(
            SpotifyToken.user_id == user.user_id).first()
        if datetime.now() >= token.expires_at:
            access_token = refresh_access_token(user.user_id, db)
        else:
            access_token = token.access_token

        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(
            'https://api.spotify.com/v1/me/player/recently-played', headers=headers)
        if response.status_code == 200:
            activities = response.json().get('items', [])
            for activity in activities:
                activity['user_id'] = user.spotify_user_id
                insert_listening_activity(activity)
    db.close()


scheduler.add_job(fetch_and_store_listening_activities, 'interval', hours=3)
