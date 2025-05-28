from openai import OpenAI
from fastapi import HTTPException
from backend.app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)

def synth(text: str) -> bytes:
    """
    Turn plain text into MP3 bytes using OpenAI TTS.
    """
    try:
        response = client.audio.speech.create(
            model="tts-1",           
            voice=settings.tts_voice,
            input=text,
            response_format="mp3",             
        )
        return response.content       
    except Exception as e:
        raise HTTPException(500, detail=f"Error generating speech: {e}")