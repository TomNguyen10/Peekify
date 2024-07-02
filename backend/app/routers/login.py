from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI
import logging
import requests

router = APIRouter()

sessions = {}
tokens = {}
SCOPE = "user-read-email user-read-private"
logging.basicConfig(level=logging.DEBUG)


@router.get("/login/spotify")
def login_spotify():
    auth_url = (
        f"https://accounts.spotify.com/authorize"
        f"?response_type=code"
        f"&client_id={SPOTIFY_CLIENT_ID}"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI}"
        f"&scope={SCOPE}"
    )
    return RedirectResponse(auth_url)


@router.get("/callback")
async def spotify_callback(request: Request, code: str):
    logging.debug(f"Received authorization code: {code}")

    if code in tokens:
        logging.error(f"Authorization code {code} has already been used.")
        raise HTTPException(
            status_code=400, detail="Authorization code already used.")

    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
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
            logging.error(f"Failed to get token: {
                          response.status_code} - {response_data}")
            raise HTTPException(
                status_code=400, detail="Failed to obtain access token")

        access_token = response_data.get("access_token")
        refresh_token = response_data.get("refresh_token")

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

        logging.debug(f"User info response status code: {
                      user_info_response.status_code}")
        logging.debug(f"User info response data: {user_info_data}")

        if user_info_response.status_code != 200:
            logging.error(f"Failed to get user info: {
                          user_info_response.status_code} - {user_info_data}")
            raise HTTPException(
                status_code=400, detail="Failed to obtain user info")

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
async def logout(response: Response, request: Request):
    session_token = request.cookies.get("session_token")
    if session_token:
        sessions.pop(session_token, None)
        response.delete_cookie(key="session_token")
        return {"message": "Logged out"}
    raise HTTPException(status_code=401, detail="Not authenticated")
