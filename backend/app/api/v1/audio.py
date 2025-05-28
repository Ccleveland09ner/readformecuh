from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, FileResponse
from backend.app.services.extract import extract_text
from backend.app.services.tts     import synth
from backend.app.storage import get_storage
from backend.app.core.config import settings
import io, os

router = APIRouter(tags=["audio"])
STORAGE = get_storage()
ALLOWED_EXT = {".pdf", ".docx", ".xml", ".txt"}
CHUNK = 1_048_576

@router.post("/to-audio")
async def to_audio(file: UploadFile, bg: BackgroundTasks):
    # 1. validate + stream upload  (same pattern as /upload)
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(400, "Unsupported file type")

    buf = io.BytesIO()
    while chunk := await file.read(CHUNK):
        buf.write(chunk)
    text = extract_text(file.filename, buf.getvalue())

    # 2. TTS – may take a couple seconds
    try:
        mp3_bytes = synth(text)
    except Exception as e:
        raise HTTPException(502, f"TTS failed: {e}")

     # ── 3. Decide how to return it based on STORAGE_MODE ───────────────
    if settings.storage_mode == "tempfile":
        # save to /tmp, schedule deletion
        path = await STORAGE.save(mp3_bytes, bg)       # returns Path
        # FileResponse reads the file in chunks without loading into RAM
        return FileResponse(
            path,
            media_type="audio/mpeg",
            filename="speech.mp3",
            headers={"Content-Disposition": 'attachment; filename="speech.mp3"'}
        )
    else:  # "stream"  (Phase-2 behaviour)
        stream = io.BytesIO(mp3_bytes)
        return StreamingResponse(
            stream,
            media_type="audio/mpeg",
            headers={"Content-Disposition": 'attachment; filename="speech.mp3"'}
        )