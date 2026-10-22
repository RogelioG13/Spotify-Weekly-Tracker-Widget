import sqlite3
from datetime import datetime, timedelta
from app.config import DB_NAME

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS play_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                track_id TEXT NOT NULL,
                track_name TEXT NOT NULL,
                artist_name TEXT NOT NULL,
                album_art TEXT,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_track_date ON play_history(track_id, played_at)")

def log_track_play(track_id: str, name: str, artist: str, album_art: str):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            "INSERT INTO play_history (track_id, track_name, artist_name, album_art) VALUES (?, ?, ?, ?)",
            (track_id, name, artist, album_art)
        )

def get_weekly_plays_for_track(track_id: str) -> int:
    seven_days_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM play_history WHERE track_id = ? AND played_at >= ?",
            (track_id, seven_days_ago)
        )
        return cursor.fetchone()[0]

def get_top_weekly_tracks(limit: int = 5) -> list[dict]:
    seven_days_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT track_id, track_name, artist_name, album_art, COUNT(*) as plays
            FROM play_history
            WHERE played_at >= ?
            GROUP BY track_id
            ORDER BY plays DESC
            LIMIT ?
        """, (seven_days_ago, limit))
        return [dict(row) for row in cursor.fetchall()]