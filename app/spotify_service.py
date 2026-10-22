import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app.config import SCOPES, CACHE_PATH

sp_oauth = SpotifyOAuth(scope=SCOPES, open_browser=True, cache_path=CACHE_PATH)

def get_client():
    token_info = sp_oauth.validate_token(sp_oauth.cache_handler.get_cached_token())
    if not token_info:
        return None
    return spotipy.Spotify(auth=token_info["access_token"])

def get_auth_url() -> str:
    return sp_oauth.get_authorize_url()

def save_token_from_code(code: str):
    sp_oauth.get_access_token(code)

def fetch_current_track() -> dict | None:
    sp = get_client()
    if not sp:
        return None
    
    current = sp.current_playback()
    if not current or not current.get("item"):
        return None

    item = current["item"]
    images = item.get("album", {}).get("images") or []
    
    return {
        "id": item["id"],
        "name": item["name"],
        "artist": ", ".join([a["name"] for a in item.get("artists", [])]),
        "album_art": images[0]["url"] if images else "",
        "is_playing": current.get("is_playing", False),
        "progress_ms": current.get("progress_ms", 0),
        "duration_ms": item.get("duration_ms", 1)
    }

def fetch_user_playlists(limit: int = 30) -> list[dict]:
    sp = get_client()
    if not sp:
        return []
    
    playlists = sp.current_user_playlists(limit=limit)
    result = []
    for p in playlists.get("items", []):
        if not p:
            continue
        images = p.get("images") or []
        image_url = images[0].get("url", "") if len(images) > 0 and images[0] else ""
        tracks_info = p.get("tracks") or {}
        
        result.append({
            "name": p.get("name", "Sin título"),
            "uri": p.get("uri", ""),
            "tracks_total": tracks_info.get("total", 0),
            "image": image_url
        })
    return result

def execute_command(action: str, context_uri: str = None):
    sp = get_client()
    if not sp:
        return
    if action == "play-context" and context_uri:
        sp.start_playback(context_uri=context_uri)
    elif action == "toggle-play":
        curr = sp.current_playback()
        if curr and curr.get("is_playing"):
            sp.pause_playback()
        else:
            sp.start_playback()
    elif action == "next":
        sp.next_track()
    elif action == "previous":
        sp.previous_track()