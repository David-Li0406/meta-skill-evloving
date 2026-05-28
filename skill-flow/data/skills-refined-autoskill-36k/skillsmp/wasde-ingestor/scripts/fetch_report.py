"""
WASDE Report Fetcher Script

Downloads WASDE reports (PDF or HTML) with retry logic and fallback sources.
"""

import os
import time
import hashlib
import requests
from typing import Dict, Optional, Tuple
from pathlib import Path


# Default configuration
DEFAULT_TIMEOUT = 30
DEFAULT_MAX_RETRIES = 5
DEFAULT_BACKOFF = [1, 2, 4, 8, 16]
USER_AGENT = "WASDE-Ingestor/0.2.0"

# Alternative sources
ALTERNATIVE_SOURCES = [
    "https://www.usda.gov/oce/commodity/wasde/wasde{yymm}.pdf",
    "https://downloads.usda.library.cornell.edu/usda-esmis/files/3t945q76s/wasde{yymm}.pdf",
]


def fetch_pdf(
    url: str,
    output_dir: str,
    retry_config: Optional[Dict] = None,
    verify_ssl: bool = True
) -> Optional[str]:
    """
    Fetch WASDE PDF report.

    Args:
        url: PDF URL
        output_dir: Directory to save the file
        retry_config: Retry configuration
        verify_ssl: Whether to verify SSL certificates

    Returns:
        str: Path to downloaded file, or None if failed
    """
    config = retry_config or {
        "max_attempts": DEFAULT_MAX_RETRIES,
        "backoff": DEFAULT_BACKOFF
    }

    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Extract filename from URL
    filename = url.split("/")[-1]
    output_path = os.path.join(output_dir, filename)

    # Check if already exists
    if os.path.exists(output_path):
        print(f"File already exists: {output_path}")
        return output_path

    # Attempt download with retries
    last_error = None
    for attempt in range(config["max_attempts"]):
        try:
            print(f"Downloading {url} (attempt {attempt + 1}/{config['max_attempts']})")

            response = requests.get(
                url,
                timeout=DEFAULT_TIMEOUT,
                verify=verify_ssl,
                headers={"User-Agent": USER_AGENT},
                stream=True
            )
            response.raise_for_status()

            # Check content type
            content_type = response.headers.get("Content-Type", "")
            if "pdf" not in content_type.lower() and "octet-stream" not in content_type.lower():
                raise ValueError(f"Unexpected content type: {content_type}")

            # Write to file
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Verify file
            if os.path.getsize(output_path) < 1000:  # PDF should be > 1KB
                os.remove(output_path)
                raise ValueError("Downloaded file too small")

            print(f"Successfully downloaded: {output_path}")
            return output_path

        except Exception as e:
            last_error = e
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < config["max_attempts"] - 1:
                backoff = config["backoff"][min(attempt, len(config["backoff"]) - 1)]
                print(f"Waiting {backoff}s before retry...")
                time.sleep(backoff)

    print(f"All attempts failed. Last error: {last_error}")
    return None


def fetch_html(
    url: str,
    retry_config: Optional[Dict] = None
) -> Optional[str]:
    """
    Fetch WASDE HTML page content.

    Args:
        url: HTML page URL
        retry_config: Retry configuration

    Returns:
        str: HTML content, or None if failed
    """
    config = retry_config or {
        "max_attempts": DEFAULT_MAX_RETRIES,
        "backoff": DEFAULT_BACKOFF
    }

    last_error = None
    for attempt in range(config["max_attempts"]):
        try:
            print(f"Fetching HTML from {url} (attempt {attempt + 1})")

            response = requests.get(
                url,
                timeout=DEFAULT_TIMEOUT,
                headers={"User-Agent": USER_AGENT}
            )
            response.raise_for_status()

            return response.text

        except Exception as e:
            last_error = e
            print(f"Attempt {attempt + 1} failed: {e}")

            if attempt < config["max_attempts"] - 1:
                backoff = config["backoff"][min(attempt, len(config["backoff"]) - 1)]
                time.sleep(backoff)

    print(f"All attempts failed. Last error: {last_error}")
    return None


def fetch_with_fallback(
    primary_url: str,
    output_dir: str,
    release_date: str,
    retry_config: Optional[Dict] = None
) -> Tuple[Optional[str], str]:
    """
    Fetch WASDE report with fallback to alternative sources.

    Args:
        primary_url: Primary PDF URL
        output_dir: Output directory
        release_date: Release date for constructing alternative URLs
        retry_config: Retry configuration

    Returns:
        tuple: (file_path, source_url) or (None, "")
    """
    # Try primary URL
    result = fetch_pdf(primary_url, output_dir, retry_config)
    if result:
        return result, primary_url

    # Parse date for alternative URL construction
    from datetime import datetime
    try:
        dt = datetime.strptime(release_date, "%Y-%m-%d")
        yymm = dt.strftime("%m%y")
    except:
        return None, ""

    # Try alternative sources
    for alt_pattern in ALTERNATIVE_SOURCES:
        alt_url = alt_pattern.format(yymm=yymm)
        if alt_url == primary_url:
            continue

        print(f"Trying alternative source: {alt_url}")
        result = fetch_pdf(alt_url, output_dir, retry_config)
        if result:
            return result, alt_url

    return None, ""


def compute_file_hash(file_path: str) -> str:
    """
    Compute SHA256 hash of a file.

    Args:
        file_path: Path to file

    Returns:
        str: SHA256 hash (first 32 characters)
    """
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()[:32]


def verify_pdf(file_path: str) -> bool:
    """
    Verify that a file is a valid PDF.

    Args:
        file_path: Path to file

    Returns:
        bool: True if valid PDF
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(5)
            return header == b'%PDF-'
    except:
        return False


# CLI interface
if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Fetch WASDE reports")
    parser.add_argument("--url", type=str, required=True, help="PDF URL to fetch")
    parser.add_argument("--output", type=str, default="./data/raw", help="Output directory")
    parser.add_argument("--retries", type=int, default=5, help="Max retry attempts")

    args = parser.parse_args()

    result = fetch_pdf(
        url=args.url,
        output_dir=args.output,
        retry_config={"max_attempts": args.retries, "backoff": DEFAULT_BACKOFF}
    )

    if result:
        file_hash = compute_file_hash(result)
        print(json.dumps({
            "success": True,
            "file_path": result,
            "file_hash": file_hash,
            "valid_pdf": verify_pdf(result)
        }, indent=2))
    else:
        print(json.dumps({"success": False}, indent=2))
