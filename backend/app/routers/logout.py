from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/logout")
def logout():
    # Redirect to Spotify logout URL
    return RedirectResponse(url="https://accounts.spotify.com/logout")
