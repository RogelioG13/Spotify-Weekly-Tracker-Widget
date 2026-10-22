from fastapi import APIRouter
from fastapi.responses import FileResponse, RedirectResponse
from app import database, spotify_service

router = APIRouter()

@router.get("/")
def serve_ui():
    if not spotify_service.get_client():
        return RedirectResponse(spotify_service.get_auth_url())
    return FileResponse("static/index.html")

@router.get("/callback")
def callback(code: str):
    spotify_service.save_token_from_code(code)
    return RedirectResponse("/")

@router.get("/api/dashboard")
def get_dashboard():
    if not spotify_service.get_client():
        return {"authenticated": False}

    track = spotify_service.fetch_current_track()
    if track:
        # Une el dato en vivo de Spotify con el conteo de nuestra BD local
        track["weekly_plays"] = database.get_weekly_plays_for_track(track["id"])

    return {
        "authenticated": True,
        "now_playing": track,
        "top_weekly": database.get_top_weekly_tracks(limit=5)
    }

@router.get("/api/playlists")
def get_playlists():
    return spotify_service.fetch_user_playlists()

@router.post("/api/control/{action}")
def player_control(action: str, uri: str | None = None):
    spotify_service.execute_command(action, context_uri=uri)
    return {"status": "ok"}