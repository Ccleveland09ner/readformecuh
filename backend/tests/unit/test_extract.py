import pytest
from pathlib import Path
from backend.app.services import extract as ex

FIX = Path(__file__).parent.parent / "fixtures"

TEST_CASES = [
    (FIX / "simple.pdf",  ex.from_pdf,  "PDF"),
    (FIX / "simple.docx", ex.from_docx, "DOCX"),
    (FIX / "simple.xml",  ex.from_xml,  "XML"),
    (FIX / "simple.txt",  ex.from_txt,  "TXT"),
]

@pytest.mark.parametrize("path,func,label", TEST_CASES)
def test_extract_basic(path, func, label):
    with open(path, "rb") as f:
        text = func(f.read())
    assert "Hello" in text, f"{label} extractor lost text"