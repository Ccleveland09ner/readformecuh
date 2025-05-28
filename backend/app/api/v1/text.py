from fastapi import APIRouter, UploadFile, HTTPException
from backend.app.services.extract import extract_text
import io, os

router = APIRouter(tags=["text"])
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".xml", ".txt"}
CHUNK_SIZE = 1_048_576

@router.post("/upload")
async def upload_file(file: UploadFile):
    # ── 1. Basic validations ────────────────────────────────────────────
    if not file.filename:
        raise HTTPException(400, "No file provided")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Unsupported file type")

    # ── 2. Read the upload into RAM, but stream in chunks ───────────────
    buffer = io.BytesIO()
    while True:
        chunk = await file.read(CHUNK_SIZE)
        if not chunk:                        
            break
        buffer.write(chunk)

    buffer.seek(0)                            
    raw_bytes = buffer.getvalue()             

    # ── 3. Delegate to services.extract (pure logic, no HTTP) ───────────
    try:
        text = extract_text(file.filename, raw_bytes)
    except ValueError as e:                   # unsupported / parse error
        raise HTTPException(415, str(e))
    except Exception as e:                    # unexpected failure
        raise HTTPException(500, f"Extraction failed: {e}")

    # ── 4. Happy path ───────────────────────────────────────────────────
    return {"text": text}
