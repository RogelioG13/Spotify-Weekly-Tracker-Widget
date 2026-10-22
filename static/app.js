// 1. Pide datos al endpoint GET /api/dashboard de Python
async function fetchDashboard() {
    try {
        const res = await fetch('/api/dashboard');
        const data = await res.json(); // Convierte el JSON de Python a un objeto JS

        if (data.now_playing) {
            const np = data.now_playing;
            document.getElementById('track-name').textContent = np.name;
            document.getElementById('artist-name').textContent = np.artist;
            if (np.album_art) document.getElementById('album-art').src = np.album_art;
            document.getElementById('weekly-badge').textContent = `${np.weekly_plays}x esta sem.`;
            
            const pct = Math.min(100, (np.progress_ms / np.duration_ms) * 100);
            document.getElementById('progress-bar').style.width = `${pct}%`;
        }

        renderTopWeekly(data.top_weekly);
    } catch (err) {
        console.error("Error obteniendo dashboard:", err);
    }
}

function renderTopWeekly(topList) {
    const container = document.getElementById('view-top');
    if (!topList || topList.length === 0) {
        container.innerHTML = `<p class="text-xs text-zinc-500 text-center py-6">Escucha música para registrar tu Top 5 semanal.</p>`;
        return;
    }

    container.innerHTML = topList.map((item, idx) => `
        <div class="flex items-center gap-3 bg-[#181818] hover:bg-zinc-800/70 border border-zinc-800/60 p-2 rounded-xl transition">
            <span class="text-xs font-bold text-zinc-500 w-4 text-center">#${idx + 1}</span>
            <img src="${item.album_art}" class="w-9 h-9 rounded-lg object-cover">
            <div class="flex-1 min-w-0">
                <p class="text-xs font-semibold text-zinc-100 truncate">${item.track_name}</p>
                <p class="text-[11px] text-zinc-400 truncate">${item.artist_name}</p>
            </div>
            <span class="text-xs font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-md">
                ${item.plays} plays
            </span>
        </div>
    `).join('');
}

// 2. Pide las playlists al endpoint GET /api/playlists de Python
async function loadPlaylists() {
    const container = document.getElementById('view-playlists');
    try {
        const res = await fetch('/api/playlists');
        const lists = await res.json();

        if (!Array.isArray(lists) || lists.length === 0) {
            container.innerHTML = `<p class="text-xs text-zinc-500 text-center py-6">No se encontraron playlists.</p>`;
            return;
        }

        container.innerHTML = lists.map(p => `
            <div onclick="sendControl('play-context', '${p.uri}')" class="cursor-pointer flex items-center justify-between gap-3 bg-[#181818] hover:bg-zinc-800 border border-zinc-800/60 p-2 rounded-xl transition">
                <div class="flex items-center gap-3 min-w-0">
                    <img src="${p.image || 'https://via.placeholder.com/40?text=♪'}" class="w-9 h-9 rounded-lg object-cover bg-zinc-800">
                    <div class="min-w-0">
                        <p class="text-xs font-semibold text-white truncate">${p.name}</p>
                        <p class="text-[10px] text-zinc-400">${p.tracks_total} canciones</p>
                    </div>
                </div>
                <span class="text-emerald-400 text-xs font-bold px-2">▶</span>
            </div>
        `).join('');
    } catch (err) {
        container.innerHTML = `<p class="text-xs text-red-400 text-center py-4">Error al conectar con el servidor.</p>`;
    }
}

// 3. Envía órdenes al endpoint POST /api/control/{action} de Python
async function sendControl(action, uri = null) {
    const url = uri 
        ? `/api/control/${action}?uri=${encodeURIComponent(uri)}` 
        : `/api/control/${action}`;
    
    await fetch(url, { method: 'POST' });
    setTimeout(fetchDashboard, 500);
}

function switchTab(tab) {
    const isTop = tab === 'top';
    document.getElementById('view-top').classList.toggle('hidden', !isTop);
    document.getElementById('view-playlists').classList.toggle('hidden', isTop);
    
    if (!isTop) loadPlaylists();

    document.getElementById('tab-top').className = isTop 
        ? 'flex-1 py-1.5 text-xs font-semibold rounded-lg bg-zinc-800 text-white transition'
        : 'flex-1 py-1.5 text-xs font-semibold rounded-lg text-zinc-400 hover:text-white transition';
    
    document.getElementById('tab-playlists').className = !isTop 
        ? 'flex-1 py-1.5 text-xs font-semibold rounded-lg bg-zinc-800 text-white transition'
        : 'flex-1 py-1.5 text-xs font-semibold rounded-lg text-zinc-400 hover:text-white transition';
}

// Inicialización
fetchDashboard();
setInterval(fetchDashboard, 4000);