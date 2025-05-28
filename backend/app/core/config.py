from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    openai_api_key: str
    tts_voice: str = "alloy"
    storage_mode: str = "stream"    
    ttl_minutes: int = 8
    tmp_dir: Path | None = None

    model_config = SettingsConfigDict(env_file=".env")

    #Summarizing
    summary_model: str = "gpt-4o-mini"

settings = Settings()
