import threading
import time
import uvicorn
import webview
from main import app
from app.config import PORT, APP_ENV

def start_server():
    # log_level="error" evita que uvicorn intente escribir en una consola inexistente
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="error")

if __name__ == "__main__":
    # 1. Inicia FastAPI en segundo plano (daemon=True hace que muera al cerrar la ventana)
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Esperar un instante a que el servidor esté listo
    time.sleep(0.8)

    # 2. Abrir la ventana emergente nativa
    title = "Spotify Tracker" if APP_ENV == "production" else "Spotify Tracker [DEV]"
    webview.create_window(
        title,
        f"http://127.0.0.1:{PORT}",
        width=390,
        height=520,
        on_top=True,
        resizable=False
    )
    webview.start()