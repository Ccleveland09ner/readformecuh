from fastapi import APIRouter, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import PlainTextResponse, StreamingResponse, FileResponse
from backend.app.services.extract   import extract_text
from backend.app.services.summarise import get_summary
from backend.app.services.tts       import synth
from backend.app.storage            import get_storage
from backend.app.core.config        import settings
import io, os

router  = APIRouter(tags=["summary"])
STORAGE = get_storage()
ALLOWED = {".pdf", ".docx", ".xml", ".txt"}
CHUNK   = 1_048_576  # 1 MB

# ─────────────────────────  /summarise  ──────────────────────────
@router.post("/summarise", response_class=PlainTextResponse)
async def summarise(file: UploadFile):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED:
        raise HTTPException(400, "Unsupported file type")

    buf = io.BytesIO()
    while chunk := await file.read(CHUNK):
        buf.write(chunk)
    text = extract_text(file.filename, buf.getvalue())

    # Guard: empty text → 422
    if not text.strip():
        raise HTTPException(
            422,
            "Could not extract readable text from this document. "
            "If it is a scanned or image-only PDF, please run OCR first."
        )

    summary = await get_summary(text)
    return summary

# ────────────────────────  /summarise-audio  ─────────────────────
@router.post("/summarise-audio")
async def summarise_audio(file: UploadFile, bg: BackgroundTasks):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED:
        raise HTTPException(400, "Unsupported file type")

    buf = io.BytesIO()
    while chunk := await file.read(CHUNK):
        buf.write(chunk)
    text = extract_text(file.filename, buf.getvalue())

    if not text.strip():
        raise HTTPException(
            422,
            "Could not extract readable text from this document. "
            "If it is a scanned or image-only PDF, please run OCR first."
        )

    summary = await get_summary(text)
    mp3     = synth(summary)

    if settings.storage_mode == "tempfile":
        path = await STORAGE.save(mp3, bg)
        return FileResponse(
            path,
            media_type="audio/mpeg",
            filename="summary.mp3",
            headers={"Content-Disposition": 'attachment; filename="summary.mp3"'}
        )

    # stream mode
    return StreamingResponse(
        io.BytesIO(mp3),
        media_type="audio/mpeg",
        headers={"Content-Disposition": 'attachment; filename="summary.mp3"'}
    )