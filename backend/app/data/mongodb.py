from pymongo.mongo_client import MongoClient
from config import MONGODB_SOURCE

mongo_client = MongoClient(MONGODB_SOURCE)
mongo_db = mongo_client['peekify']


def insert_listening_activity(activity):
    mongo_db.listening_activity_logs.insert_one(activity)


activity = {
    "user_id": "spotify_user_id",
    "played_at": "2023-06-23T10:00:00Z",
    "track": {
        "id": "track_id",
        "name": "track_name",
        "album": {
            "id": "album_id",
            "name": "album_name"
        },
        "artists": [
            {
                "id": "artist_id",
                "name": "artist_name"
            }
        ]
    },
    "context": {
        "type": "playlist",
        "uri": "spotify:playlist:playlist_id",
        "external_urls": {
            "spotify": "https://open.spotify.com/playlist/playlist_id"
        }
    }
}

insert_listening_activity(activity)
