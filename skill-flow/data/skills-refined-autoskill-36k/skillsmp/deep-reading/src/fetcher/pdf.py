"""PDF content fetcher using PyMuPDF (fitz)"""
import subprocess
import json
import hashlib
import shutil
from pathlib import Path
from typing import Optional, Tuple
import sys

sys.path.insert(0, str(Path.home() / ".deep-reading"))
from config import CACHE_DIR


def generate_pdf_id(pdf_path: Path) -> str:
    """Generate a unique ID for a PDF based on path hash"""
    path_str = str(pdf_path.resolve())
    hash_digest = hashlib.md5(path_str.encode()).hexdigest()[:12]
    return hash_digest


def get_cache_dir(pdf_id: str) -> Path:
    """Get cache directory for a PDF"""
    cache_dir = CACHE_DIR / "pdf" / pdf_id
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def extract_text_with_pymupdf(pdf_path: Path, txt_path: Path) -> str:
    """Extract text using PyMuPDF (fitz)"""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise ImportError("PyMuPDF not installed. Run: pip install PyMuPDF")

    doc = fitz.open(str(pdf_path))
    text_parts = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        if text.strip():
            text_parts.append(f"--- Page {page_num + 1} ---\n{text}")

    doc.close()

    full_text = "\n\n".join(text_parts)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    return full_text


def extract_metadata_with_pymupdf(pdf_path: Path) -> dict:
    """Extract metadata using PyMuPDF"""
    try:
        import fitz
    except ImportError:
        raise ImportError("PyMuPDF not installed. Run: pip install PyMuPDF")

    doc = fitz.open(str(pdf_path))
    metadata = doc.metadata or {}
    page_count = len(doc)
    doc.close()

    return {
        "title": metadata.get("title", ""),
        "author": metadata.get("author", ""),
        "subject": metadata.get("subject", ""),
        "creator": metadata.get("creator", ""),
        "producer": metadata.get("producer", ""),
        "page_count": page_count,
    }


def fetch_metadata(pdf_path: Path, pdf_id: str) -> dict:
    """Fetch PDF metadata"""
    cache_dir = get_cache_dir(pdf_id)

    # Extract metadata
    pdf_metadata = extract_metadata_with_pymupdf(pdf_path)

    # Use filename as title if not in metadata
    title = pdf_metadata.get("title") or pdf_path.stem
    # Clean up title from Z-Library naming
    if "(Z-Library)" in title:
        title = title.replace("(Z-Library)", "").strip()

    author = pdf_metadata.get("author") or "Unknown"
    # Clean author from parentheses format like "Max Bennett"
    if "(" in str(pdf_path.stem) and ")" in str(pdf_path.stem):
        # Try to extract author from filename pattern: "Title (Author)"
        import re
        match = re.search(r'\(([^)]+)\)\s*(?:\(Z-Library\))?$', pdf_path.stem)
        if match and not pdf_metadata.get("author"):
            author = match.group(1)

    metadata = {
        "id": pdf_id,
        "title": title,
        "author": author,
        "page_count": pdf_metadata.get("page_count", 0),
        "path": str(pdf_path),
        "subject": pdf_metadata.get("subject", ""),
    }

    # Save to cache
    with open(cache_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return metadata


def fetch_text(pdf_path: Path, pdf_id: str) -> Path:
    """Extract text from PDF"""
    cache_dir = get_cache_dir(pdf_id)
    txt_path = cache_dir / "content.txt"

    if txt_path.exists():
        print(f"Text already cached: {txt_path}")
        return txt_path

    print("Extracting text from PDF...")
    extract_text_with_pymupdf(pdf_path, txt_path)
    print(f"Text extracted: {txt_path}")

    return txt_path


def copy_pdf_to_cache(pdf_path: Path, pdf_id: str) -> Path:
    """Copy PDF to cache for reference"""
    cache_dir = get_cache_dir(pdf_id)
    cached_pdf = cache_dir / "source.pdf"

    if not cached_pdf.exists():
        shutil.copy2(pdf_path, cached_pdf)

    return cached_pdf


def fetch_pdf(path: str) -> dict:
    """Main entry point: fetch all content from PDF file"""
    pdf_path = Path(path).resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if not pdf_path.suffix.lower() == ".pdf":
        raise ValueError(f"Not a PDF file: {pdf_path}")

    pdf_id = generate_pdf_id(pdf_path)
    print(f"Processing PDF: {pdf_path.name} (ID: {pdf_id})")

    # Fetch all components
    metadata = fetch_metadata(pdf_path, pdf_id)
    txt_path = fetch_text(pdf_path, pdf_id)
    cached_pdf = copy_pdf_to_cache(pdf_path, pdf_id)

    cache_dir = get_cache_dir(pdf_id)

    return {
        "id": f"pdf_{pdf_id}",
        "type": "pdf",
        "pdf_id": pdf_id,
        "metadata": metadata,
        "cache_dir": str(cache_dir),
        "txt_path": str(txt_path),
        "pdf_path": str(cached_pdf),
        "original_path": str(pdf_path),
    }
