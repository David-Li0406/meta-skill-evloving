"""Fetcher CLI"""
import sys
import argparse
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path.home() / ".deep-reading"))

from fetcher.youtube import fetch_youtube, extract_video_id
from fetcher.pdf import fetch_pdf
from db import get_connection, init_db
from models import SourceType, ProcessingState

def detect_source_type(path_or_url: str) -> str:
    """Detect source type from path or URL"""
    # Check if it's a local file path
    p = Path(path_or_url)
    if p.exists() or path_or_url.endswith(".pdf"):
        if path_or_url.lower().endswith(".pdf"):
            return "pdf"

    # Check for directory containing PDF
    if p.is_dir():
        pdf_files = list(p.glob("*.pdf"))
        if pdf_files:
            return "pdf"

    # URL-based detection
    if "youtube.com" in path_or_url or "youtu.be" in path_or_url:
        return "youtube"
    elif path_or_url.endswith(".mp3") or "podcast" in path_or_url.lower():
        return "podcast"
    else:
        return "web"

def fetch(path_or_url: str):
    """Fetch content from path or URL"""
    init_db()

    source_type = detect_source_type(path_or_url)
    print(f"Detected source type: {source_type}")

    if source_type == "youtube":
        result = fetch_youtube(path_or_url)

        # Save to database
        conn = get_connection()
        conn.execute("""
            INSERT OR REPLACE INTO sources
            (id, type, url, title, author, duration, cache_path, processing_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result["id"],
            source_type,
            path_or_url,
            result["metadata"]["title"],
            result["metadata"]["author"],
            result["metadata"]["duration"],
            result["cache_dir"],
            "ready"
        ))
        conn.commit()
        conn.close()

        print(f"\n✓ Downloaded: {result['metadata']['title']}")
        print(f"  ID: {result['id']}")
        print(f"  Duration: {result['metadata']['duration']}s")
        print(f"  Cache: {result['cache_dir']}")
        print(f"\nTo process: python3 -m processor.cli {result['id']}")

    elif source_type == "pdf":
        # Handle directory containing PDF
        p = Path(path_or_url)
        if p.is_dir():
            pdf_files = list(p.glob("*.pdf"))
            if pdf_files:
                path_or_url = str(pdf_files[0])
            else:
                print("No PDF files found in directory")
                sys.exit(1)

        result = fetch_pdf(path_or_url)

        # Save to database
        conn = get_connection()
        conn.execute("""
            INSERT OR REPLACE INTO sources
            (id, type, url, title, author, duration, cache_path, processing_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result["id"],
            source_type,
            result["original_path"],
            result["metadata"]["title"],
            result["metadata"]["author"],
            result["metadata"].get("page_count", 0),  # Use page_count as duration placeholder
            result["cache_dir"],
            "ready"
        ))
        conn.commit()
        conn.close()

        print(f"\n✓ Processed: {result['metadata']['title']}")
        print(f"  ID: {result['id']}")
        print(f"  Author: {result['metadata']['author']}")
        print(f"  Pages: {result['metadata'].get('page_count', 'Unknown')}")
        print(f"  Cache: {result['cache_dir']}")
        print(f"\nTo process: python3 -m processor.cli {result['id']}")

    else:
        print(f"Source type '{source_type}' not yet implemented")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Fetch content")
    parser.add_argument("url", help="URL to fetch")
    args = parser.parse_args()

    fetch(args.url)

if __name__ == "__main__":
    main()
