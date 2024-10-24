from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.postgresql import get_db
from config import SPOTIFY_API_BASE_URL
from utils.top_items import (
    get_songs_per_day,
    get_top_songs_this_week,
    get_top_albums_this_week,
    get_top_artists_this_week
)
import requests


router = APIRouter()


@router.get("/top_items/songs-per-day")
def songs_per_day(user_spotify_id: str, db: Session = Depends(get_db)):
    try:
        result = get_songs_per_day(db, user_spotify_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching songs per day: {str(e)}")


@router.get("/top_items/top-songs-this-week")
def top_songs_this_week(user_spotify_id: str, limit: int = 5, db: Session = Depends(get_db)):
    try:
        result = get_top_songs_this_week(db, user_spotify_id, limit)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching top songs: {str(e)}")


@router.get("/top_items/top-albums-this-week")
def top_songs_this_week(user_spotify_id: str, limit: int = 5, db: Session = Depends(get_db)):
    try:
        result = get_top_albums_this_week(db, user_spotify_id, limit)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching top songs: {str(e)}")


@router.get("/top_items/top-artists-this-week")
def top_artists_this_week(user_spotify_id: str, limit: int = 5, db: Session = Depends(get_db)):
    try:
        result = get_top_artists_this_week(db, user_spotify_id, limit)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching top artists: {str(e)}")


@router.get("/top_items/top-tracks")
def top_tracks(access_token: str, limit: int = 5, time_range: str = "medium_term"):
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"limit": limit, "time_range": time_range}
        response = requests.get(
            f"{SPOTIFY_API_BASE_URL}/me/top/tracks", headers=headers, params=params)
        return response.json()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching top tracks from API: {str(e)}")


@router.get("/top_items/top-artists")
def top_tracks(access_token: str, limit: int = 5, time_range: str = "medium_term"):
    try:
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"limit": limit, "time_range": time_range}
        response = requests.get(
            f"{SPOTIFY_API_BASE_URL}/me/top/artists", headers=headers, params=params)
        return response.json()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching top artists from API: {str(e)}")
