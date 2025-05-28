from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import text as text_router 
from .api.v1 import audio as audio_router
from .api.v1 import summary as summary_router

app = FastAPI(title="readformecuh", version="0.1.0")

# CORS – dev-only; tighten later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text_router.router, prefix="/api/v1")
app.include_router(audio_router.router, prefix="/api/v1")
app.include_router(summary_router.router, prefix="/api/v1")   

@app.get("/", tags=["health"])
def root():
    return {"status": "ok"}

# placeholder – will mount text router in Phase 1