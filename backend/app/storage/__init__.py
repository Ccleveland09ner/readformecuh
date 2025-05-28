from backend.app.core.config import settings
from .stream    import StreamStorage
from .tempfile  import TempFileStorage
from pathlib    import Path
import os

def get_storage():
    mode = settings.storage_mode
    if mode == "stream":
        return StreamStorage()
    if mode == "tempfile":
        tmp = settings.tmp_dir or Path(os.getenv("TMP", "/tmp")) / "readformecuh"
        return TempFileStorage(tmp, settings.ttl_minutes)
    raise ValueError(f"Unknown STORAGE_MODE: {mode}")
