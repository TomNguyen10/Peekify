from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
POSTGRESQL_SOURCE = os.getenv("POSTGRESQL_SOURCE")
