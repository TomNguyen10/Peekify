from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI_LOCAL, SPOTIFY_REDIRECT_URI_DEPLOY
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from schemas.spotify_tokens import SpotifyTokenCreate
from utils.user import get_user_by_spotify_id, create_user
from utils.spotify_tokens import create_or_update_spotify_token
from utils.top_items import get_user_top_items_from_spotify
from data.postgresql import get_db
from datetime import datetime, timedelta
import logging
import requests

router = APIRouter()

sessions = {}
tokens = {}
SCOPE = "user-read-email user-read-private user-read-recently-played user-top-read"
logging.basicConfig(level=logging.DEBUG)


@router.get("/login/spotify")
def login_spotify():
    auth_url = (
        f"https://accounts.spotify.com/authorize"
        f"?response_type=code"
        f"&client_id={SPOTIFY_CLIENT_ID}"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI_DEPLOY}"
        f"&scope={SCOPE}"
    )
    return RedirectResponse(auth_url)


@router.get("/callback")
async def spotify_callback(request: Request, code: str, db: Session = Depends(get_db)):
    logging.debug(f"Received authorization code: {code}")

    if code in tokens:
        logging.error(f"Authorization code {code} has already been used.")
        raise HTTPException(
            status_code=400, detail="Authorization code already used.")

    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI_DEPLOY,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(token_url, data=payload, headers=headers)
        response_data = response.json()

        logging.debug(f"Token request payload: {payload}")
        logging.debug(f"Token request headers: {headers}")
        logging.debug(f"Token response status code: {response.status_code}")
        logging.debug(f"Token response data: {response_data}")

        if response.status_code != 200:
            logging.error(f"""Failed to get token: {
                          response.status_code} - {response_data}""")

            raise HTTPException(
                status_code=400, detail="Failed to obtain access token")

        access_token = response_data.get("access_token")
        refresh_token = response_data.get("refresh_token")
        expires_in = response_data.get("expires_in")
        tokens[code] = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        logging.debug(f"Access token obtained: {access_token}")

        user_info_url = "https://api.spotify.com/v1/me"
        user_info_headers = {
            "Authorization": f"Bearer {access_token}"
        }

        user_info_response = requests.get(
            user_info_url, headers=user_info_headers)
        user_info_data = user_info_response.json()

        logging.error(f"""User info response status code: {
            user_info_response.status_code}""")
        logging.debug(f"User info response data: {user_info_data}")

        if user_info_response.status_code != 200:
            logging.error(f"""Failed to get user info: {
                          user_info_response.status_code} - {user_info_data}""")
            raise HTTPException(
                status_code=400, detail="Failed to obtain user info")
        spotify_user_id = user_info_data.get('id')
        user = get_user_by_spotify_id(db, spotify_user_id)
        if not user:
            user_create = UserCreate(
                id=spotify_user_id,
                username=user_info_data.get('display_name'),
                email=user_info_data.get('email'),
                country=user_info_data.get('country'),
                images=str(user_info_data.get('images')),
                profile_url=user_info_data.get(
                    'external_urls', {}).get('spotify')
            )
            user = create_user(db, user_create)
            logging.info(f"""Created new user with ID: {
                         user.id}""")

        token_create = SpotifyTokenCreate(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=response_data.get('token_type'),
            expires_at=datetime.now() + timedelta(seconds=expires_in),
            scope=response_data.get('scope')
        )
        create_or_update_spotify_token(
            db, user.id, token_create)
        logging.info(
            f"Created/Updated Spotify token for user ID: {user.id}")

        top_items = {
            "short_term": {
                "top_artists": get_user_top_items_from_spotify(access_token, "artists", "short_term"),
                "top_tracks": get_user_top_items_from_spotify(access_token, "tracks", "short_term")
            },
            "medium_term": {
                "top_artists": get_user_top_items_from_spotify(access_token, "artists", "medium_term"),
                "top_tracks": get_user_top_items_from_spotify(access_token, "tracks", "medium_term")
            },
            "long_term": {
                "top_artists": get_user_top_items_from_spotify(access_token, "artists", "long_term"),
                "top_tracks": get_user_top_items_from_spotify(access_token, "tracks", "long_term")
            }
        }

        user_info_data["top_items"] = top_items
        logging.info(f"User info data: {user_info_data}")
        return JSONResponse(content=user_info_data)

    except Exception as e:
        logging.error(f"Error during token exchange: {str(e)}")
        raise HTTPException(status_code=400, detail="Token exchange failed")


@router.get("/user")
async def get_user(request: Request):
    session_token = request.cookies.get("session_token")
    if session_token and session_token in sessions:
        return {"user_info": sessions[session_token]}
    raise HTTPException(status_code=401, detail="Not authenticated")


@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("session_token")
    return JSONResponse(content={"message": "Logged out successfully"})
