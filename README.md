# ReadForMeCuh

Turn documents into **text, summaries, and audio** you can stream or download  
— with optional TTL clean-up so temp files never clog your server.

<table>
<tr><td>Backend</td><td>FastAPI &middot; OpenAI &middot; Python 3.11</td></tr>
<tr><td>Front-end (coming)</td><td>React 18 · TypeScript · Vite</td></tr>
</table>

---

## Features

| Capability | Route | Notes |
|------------|-------|-------|
| **Upload + extract text** | `POST /api/v1/upload` | Streams large files in 1 MB chunks, returns raw text. |
| **Full document → audio** | `POST /api/v1/to-audio` | Streams MP3 or saves to temp dir; auto-deletes after *TTL*. |
| **AI summary (~200 words)** | `POST /api/v1/summarise` | Uses OpenAI Chat completions, model set via `.env`. |
| **Summary → audio** | `POST /api/v1/summarise-audio` | Combines summary + TTS pipeline. |
| **Storage modes** | `.env → STORAGE_MODE` | `stream` (RAM) • `tempfile` (disk + TTL) • ready for `persistent`. |
| **File types** | PDF · DOCX · XML · TXT | Text-layer PDFs only (OCR fallback is TODO). |
| **Error handling** | 400 / 422 / 502 | Empty doc returns 422; OpenAI network issues return 502. |
| **Tests** | `pytest` | Unit (extractors) + integration (key endpoints). |

---

## Project layout

backend/
│ app/
│ ├─ api/
│ │ └─ v1/ # upload, audio, summary routers
│ ├─ core/ # config.py reads .env
│ ├─ services/ # extract.py · tts.py · summarise.py
│ └─ storage/ # stream.py · tempfile.py · init.py
tests/
└─ frontend/ # Vite–React app