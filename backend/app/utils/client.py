import spotipy


def get_spotify_client(access_token: str):
    return spotipy.Spotify(auth=access_token)


def fetch_recently_played(spotify_client):
    return spotify_client.current_user_recently_played()
