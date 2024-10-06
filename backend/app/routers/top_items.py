from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.postgresql import get_db
from utils.top_items import (
    get_songs_per_day,
    get_top_songs_this_week,
    get_top_albums_this_week,
    get_top_artists_this_week
)

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
