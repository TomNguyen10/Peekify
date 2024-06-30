from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
import secrets
import uvicorn

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Spotify OAuth Config
SPOTIFY_CLIENT_ID = "afbb70c2c3f1418ab00bdfc52ab754f7"
SPOTIFY_CLIENT_SECRET = "82417ed738434bd19305fda377edd093"
# Updated to match frontend port
SPOTIFY_REDIRECT_URI = "http://localhost:5173/callback"

# In-memory storage for simplicity
sessions = {}


@app.get("/login/spotify")
async def spotify_login():
    authorization_url = (
        f"https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI}"
        "&scope=user-read-private%20user-read-email"
    )
    return {"redirect_url": authorization_url}


@app.get("/callback")
async def spotify_callback(code: str, response: Response):
    params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }

    async with httpx.AsyncClient() as client:
        token_response = await client.post("https://accounts.spotify.com/api/token", data=params)

    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data["access_token"]

        async with httpx.AsyncClient() as client:
            user_response = await client.get("https://api.spotify.com/v1/me", headers={
                "Authorization": f"Bearer {access_token}"
            })

        if user_response.status_code == 200:
            user_info = user_response.json()
            session_token = secrets.token_hex(16)
            sessions[session_token] = user_info

            response.set_cookie(key="session_token",
                                value=session_token, httponly=True)
            return {"message": "Login successful", "user_info": user_info}
        else:
            print(f"Failed to fetch user info: {
                  user_response.status_code} - {user_response.text}")

    else:
        print(f"Failed to get token: {
              token_response.status_code} - {token_response.text}")
        print("Token request params:", params)

    raise HTTPException(status_code=token_response.status_code,
                        detail="Failed to authenticate with Spotify")


@app.get("/user")
async def get_user(request: Request):
    session_token = request.cookies.get("session_token")
    if session_token and session_token in sessions:
        return {"user_info": sessions[session_token]}
    raise HTTPException(status_code=401, detail="Not authenticated")


@app.post("/logout")
async def logout(response: Response, request: Request):
    session_token = request.cookies.get("session_token")
    if session_token:
        sessions.pop(session_token, None)
        response.delete_cookie(key="session_token")
        return {"message": "Logged out"}
    raise HTTPException(status_code=401, detail="Not authenticated")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
