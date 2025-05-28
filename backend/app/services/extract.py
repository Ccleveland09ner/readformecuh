from pathlib import Path
import re
import io

# ---------- PDF (PyMuPDF) ----------
def from_pdf(blob: bytes) -> str:
    import fitz  # PyMuPDF
    text = ""
    with fitz.open(stream=blob, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# ---------- DOCX ----------
def from_docx(blob: bytes) -> str:
    """
    Return all visible paragraph text in document order.
    Ignores empty lines and weird control chars.
    """
    from docx import Document
    import io

    doc = Document(io.BytesIO(blob))
    parts = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    text  = "\n".join(parts)

    # Collapse excessive internal whitespace (optional)
    text  = re.sub(r"\s{2,}", " ", text)
    return text

# ---------- TXT ----------
def from_txt(blob: bytes) -> str:
    return blob.decode("utf-8", errors="replace")

# ---------- XML ----------
def from_xml(blob: bytes) -> str:
    import xml.etree.ElementTree as ET
    root = ET.fromstring(blob)
    # Collect all text nodes
    return "\n".join(t.strip() for t in root.itertext() if t.strip())

# ---------- Dispatcher ----------
def extract_text(filename: str, blob: bytes) -> str:
    ext = Path(filename).suffix.lower()
    match ext:
        case ".pdf":  return from_pdf(blob)
        case ".docx": return from_docx(blob)
        case ".xml":  return from_xml(blob)
        case ".txt":  return from_txt(blob)
        case _:       raise ValueError(f"Unsupported file type: {ext}")
