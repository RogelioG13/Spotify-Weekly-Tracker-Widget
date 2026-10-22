import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app import database, spotify_service
from app.routes import router

last_logged_track_id = None

async def background_tracker():
    global last_logged_track_id
    while True:
        try:
            track = spotify_service.fetch_current_track()
            if track and track["is_playing"]:
                if track["id"] != last_logged_track_id and track["progress_ms"] > 15000:
                    database.log_track_play(
                        track["id"], track["name"], track["artist"], track["album_art"]
                    )
                    last_logged_track_id = track["id"]
        except Exception as e:
            print(f"Error en tracker: {e}")
        await asyncio.sleep(15)

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init_db()
    task = asyncio.create_task(background_tracker())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

# Sirve la carpeta 'static' para que index.html pueda cargar app.js
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)