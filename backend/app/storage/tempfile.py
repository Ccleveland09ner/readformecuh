from pathlib import Path
from fastapi import BackgroundTasks
import uuid, asyncio, aiofiles, os

class TempFileStorage:
    def __init__(self, tmp_dir: Path | None, ttl: int):
        self.tmp_dir = tmp_dir or Path(os.getenv("TMP", "/tmp"))
        self.ttl     = ttl

    async def save(self, data: bytes, bg: BackgroundTasks) -> Path:
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        path = self.tmp_dir / f"{uuid.uuid4()}.mp3"
        async with aiofiles.open(path, "wb") as f:
            await f.write(data)

        # schedule deletion
        bg.add_task(self._delete_after_ttl, path)
        return path

    async def _delete_after_ttl(self, path: Path):
        await asyncio.sleep(self.ttl * 60)
        path.unlink(missing_ok=True)