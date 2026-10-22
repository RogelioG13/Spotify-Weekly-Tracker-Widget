import os
from dotenv import load_dotenv

load_dotenv()

SCOPES = (
    "user-read-currently-playing "
    "user-read-playback-state "
    "user-modify-playback-state "
    "playlist-read-private "
    "playlist-read-collaborative"
)
DB_NAME = "spotify_stats.db"
CACHE_PATH = ".spotify_cache"