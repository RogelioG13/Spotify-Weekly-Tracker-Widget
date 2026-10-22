import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")
PORT = int(os.getenv("PORT", 8000))


# Si estás en prod usa spotify_prod.db, si estás en dev usa spotify_dev.db
DB_NAME = os.getenv("DB_NAME", f"spotify_{APP_ENV}.db")
CACHE_PATH = ".spotify_cache"

SCOPES = (
    "user-read-currently-playing "
    "user-read-playback-state "
    "user-modify-playback-state "
    "playlist-read-private "
    "playlist-read-collaborative"
)
DB_NAME = "spotify_stats.db"
CACHE_PATH = ".spotify_cache"