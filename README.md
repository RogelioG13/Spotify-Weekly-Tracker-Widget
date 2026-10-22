# Spotify Weekly Tracker Widget

Aplicación ligera de escritorio y API local construida con **FastAPI**, **SQLite** y **Tailwind CSS** que extiende las capacidades de la API oficial de Spotify.

Permite visualizar en tiempo real la pista en reproducción, controlar el reproductor (Spotify Connect), explorar playlists personales y llevar un **conteo exacto de reproducciones semanales y un Top 5 de los últimos 7 días** (métricas que la API de Spotify no entrega de forma nativa).

---

## Características Principales

- **Reproductor en Tiempo Real:** Muestra carátula, título, artista, barra de progreso y controles de reproducción (`Play/Pause`, `Siguiente`, `Anterior`).
- **Contador de Escuchas Semanal:** Muestra cuántas veces has reproducido la canción actual durante los últimos 7 días.
- **Top 5 de la Semana:** Ranking dinámico calculado mediante un recolector asíncrono en segundo plano (`polling`) almacenado localmente en SQLite.
- **Lanzador de Playlists:** Acceso rápido a tus listas de reproducción privadas y colaborativas.
- **Arquitectura en Capas:** Diseño modular con alta cohesión y bajo acoplamiento (separación entre rutas HTTP, adaptador de servicios externos, persistencia de datos y cliente web).

---

## Estructura del Proyecto

```text
spotify-widget/
├── .env.example             # Plantilla de variables de entorno
├── .gitignore               # Archivos excluidos del control de versiones
├── requirements.txt         # Dependencias de Python
├── main.py                  # Punto de entrada: servidor FastAPI y tarea en segundo plano
├── app/                     # Paquete del Backend (Arquitectura en capas)
│   ├── __init__.py
│   ├── config.py            # Configuración global y lectura de variables de entorno
│   ├── database.py          # Capa de persistencia: consultas y esquema SQLite
│   ├── spotify_service.py   # Capa de servicio: cliente OAuth 2.0 y llamadas a Spotify API
│   └── routes.py            # Capa controladora: endpoints REST que comunican con el frontend
└── static/                  # Cliente Frontend
    ├── index.html           # Interfaz de usuario estilo widget (Tailwind CSS)
    └── app.js               # Lógica del cliente y consumo de la API local vía fetch()
```

---

## Requisitos Previos

- **Python 3.10+** instalado en el sistema.
- Una cuenta de **Spotify** (se requiere _Spotify Premium_ para usar los controles remotos de reproducción; las estadísticas y lectura funcionan en cualquier cuenta).
- Credenciales de aplicación creadas en el [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).

---

## Instalación y Configuración

### 1. Clonar el repositorio y crear el entorno virtual

En tu terminal (PowerShell o CMD):

```powershell
git clone <URL_DE_TU_REPOSITORIO>
cd spotify-widget

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (PowerShell)
.\venv\Scripts\Activate.ps1
# (En CMD usa: .\venv\Scripts\activate)
```

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 3. Configurar credenciales de Spotify (`.env`)

1. Entra al [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) y crea una nueva aplicación.
2. En la configuración de la app, busca el apartado **Redirect URIs**, agrega exactamente la siguiente dirección y guarda los cambios:
   ```text
   [http://127.0.0.1:8000/callback](http://127.0.0.1:8000/callback)
   ```
3. En la raíz del proyecto, crea un archivo llamado `.env` (puedes duplicar `.env.example`) con tus claves:
   ```env
   SPOTIPY_CLIENT_ID=tu_client_id_aqui
   SPOTIPY_CLIENT_SECRET=tu_client_secret_aqui
   SPOTIPY_REDIRECT_URI=[http://127.0.0.1:8000/callback](http://127.0.0.1:8000/callback)
   ```

---

## Ejecución

### Paso 1: Iniciar el servidor Backend

Con tu entorno virtual activado, levanta el servidor local con Uvicorn:

```powershell
uvicorn main:app --port 8000
```

_(La primera vez que accedas a `http://127.0.0.1:8000`, se abrirá tu navegador para autorizar los permisos de tu cuenta de Spotify y se generará el archivo local `.spotify_cache`)._

### Paso 2: Abrir en modo Widget Flotante

Tienes dos opciones para abrir la ventana sin que interfiera con tu fondo de pantalla:

**Opción A: Modo App nativo del navegador (Ligero)**
Ejecuta en otra terminal:

```powershell
start msedge --app=[http://127.0.0.1:8000](http://127.0.0.1:8000) --window-size=390,480
```

**Opción B: Ventana "Always on Top" con PyWebView**
Si deseas que el widget permanezca siempre visible sobre otras ventanas, ejecuta:

```powershell
python -c "import webview; webview.create_window('Spotify Tracker', '[http://127.0.0.1:8000](http://127.0.0.1:8000)', width=390, height=500, on_top=True, resizable=False); webview.start()"
```

---

## Endpoints de la API Local

Con el servidor encendido, puedes explorar y probar la documentación interactiva generada por FastAPI (Swagger UI) en `http://127.0.0.1:8000/docs`.

| Método | Ruta                    | Descripción                                                                                                 |
| ------ | ----------------------- | ----------------------------------------------------------------------------------------------------------- |
| `GET`  | `/`                     | Sirve la interfaz principal o redirige al flujo OAuth de Spotify.                                           |
| `GET`  | `/api/dashboard`        | Devuelve el estado actual de reproducción, el conteo semanal de la pista activa y el Top 5 semanal en JSON. |
| `GET`  | `/api/playlists`        | Lista las playlists del usuario con portada, nombre y total de canciones.                                   |
| `POST` | `/api/control/{action}` | Ejecuta comandos en Spotify Connect (`toggle-play`, `next`, `previous`, `play-context`).                    |

---

## Seguridad y Privacidad

Este proyecto está configurado para operar localmente. El archivo `.gitignore` excluye explícitamente:

- `.env` (Credenciales de API).
- `.spotify_cache` (Tokens de sesión OAuth 2.0).
- `*.db` (Base de datos SQLite con tu historial de reproducción).
