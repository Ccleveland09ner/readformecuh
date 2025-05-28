from fastapi.testclient import TestClient
from pathlib import Path
from backend.app.main import app      # FastAPI entry

client = TestClient(app)
FIX = Path(__file__).parent.parent / "fixtures"

def test_upload_pdf():
    pdf = FIX / "simple.pdf"
    
    resp = client.post(
        "/api/v1/upload",              # adjust path if needed
        files={"file": pdf.open("rb")},
    )
    assert resp.status_code == 200
    assert "Hello" in resp.json()["text"]
