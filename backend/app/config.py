from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
POSTGRESQL_SOURCE = os.getenv("POSTGRESQL_SOURCE")
MONGODB_SOURCE = os.getenv("MONGODB_SOURCE")
SPOTIFY_API_BASE_URL = os.getenv("SPOTIFY_API_BASE_URL")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL")
