<p align="center">
  <a href="https://github.com/AndresBlancoSierra/what">
    <img src="https://raw.githubusercontent.com/AndresBlancoSierra/what/main/profile.svg" alt="WHAT? — what@arch">
  </a>
</p>

# WHAT? — Aprende idiomas con canciones

WHAT? es una app de **aprendizaje de idiomas a través de música**: busca una
canción, la descarga, la transcribe con Whisper, extrae la letra (Genius) y te
la muestra sincronizada con el audio y traducciones, para que aprendas
vocabulario escuchando.

Backend **FastAPI** (Python) + Frontend **React/Vite**.

---

## 🚀 Cómo correrlo

```bash
cd ~/Proyects/what
./what-question
```

Levanta automáticamente:

| Servicio | URL |
| --- | --- |
| Frontend | http://localhost:5174 |
| Backend API | http://localhost:8001 |
| API docs (Swagger) | http://localhost:8001/docs |

Puertos configurables con `WHAT_BACKEND_PORT` y `WHAT_FRONTEND_PORT`. Ctrl+C
detiene ambos.

---

## 🧠 Cómo funciona

1. **Buscar**: busca canciones por nombre/artista.
2. **Descargar**: obtiene el audio con `yt-dlp`.
3. **Transcribir**: separa voz/instrumental y transcribe con `faster-whisper`.
4. **Letra**: la sincroniza con la letra oficial de Genius.
5. **Exportar**: puedes exportar lo aprendido (p. ej. a Anki).

### Stack

- **Backend**: FastAPI, SQLAlchemy (async) + SQLite, yt-dlp, faster-whisper, httpx.
- **Frontend**: React 19, TypeScript, Vite, Tailwind 4, TanStack Query,
  React Router, Framer Motion.

---

## 📁 Estructura

```
what/
├── what-question        ← lanzador (backend + frontend)
├── src/what/
│   ├── api/             ← rutas FastAPI
│   ├── core/            ← downloader, transcriber, aligner, lyrics, exporter
│   ├── config/          ← carga de configs/default.yaml
│   └── database/        ← modelos y sesión SQLite
├── what-app/            ← frontend React
│   └── src/{pages,components}
└── configs/default.yaml ← configuración (modelo Whisper, tokens, rutas)
```

---

## ⚙️ Configuración

`configs/default.yaml`:

| Clave | Valor por defecto | Qué es |
| --- | --- | --- |
| `whisper.model_size` | `large-v3` | Modelo Whisper |
| `whisper.device` | `auto` | CPU/GPU |
| `storage.data_dir` | `data/songs` | Audios descargados |
| `storage.anki_dir` | `~/Documents/Anki` | Exportación Anki |
| `database.url` | `sqlite+aiosqlite:///data/what.db` | Base de datos |

Requiere Python ≥ 3.12 y se maneja con `uv` (`uv run uvicorn what.api:app`).

---

## 🗃️ Repos de referencia

Este proyecto nació de investigar y analizar repositorios de GitHub sobre
transcripción y aprendizaje de idiomas. Los clones de análisis (`repos/`) se
excluyeron del repositorio final.
