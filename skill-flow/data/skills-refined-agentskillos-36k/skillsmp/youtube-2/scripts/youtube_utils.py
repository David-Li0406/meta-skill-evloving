#!/usr/bin/env python3
"""
YouTube link cleaning and caching utilities.

This script provides helper functions for:
- Cleaning YouTube URLs to short form (youtu.be/<id>)
- Extracting video IDs from various YouTube URL formats
- Managing transcript cache in .youtube directory
"""

import re
import json
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str) -> str | None:
    """
    Extract YouTube video ID from various URL formats.

    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://m.youtube.com/watch?v=VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/v/VIDEO_ID

    Args:
        url: YouTube URL string

    Returns:
        Video ID string or None if not found
    """
    # Handle short URL format
    if 'youtu.be/' in url:
        match = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', url)
        if match:
            return match.group(1)

    # Handle standard watch URL
    parsed = urlparse(url)
    if parsed.hostname in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
        if parsed.path == '/watch':
            query_params = parse_qs(parsed.query)
            if 'v' in query_params:
                return query_params['v'][0]
        # Handle embed URLs
        elif parsed.path.startswith('/embed/'):
            return parsed.path.split('/')[2]
        # Handle /v/ URLs
        elif parsed.path.startswith('/v/'):
            return parsed.path.split('/')[2]

    return None


def clean_youtube_url(url: str) -> str | None:
    """
    Convert any YouTube URL to clean short form: https://youtu.be/<id>

    Args:
        url: YouTube URL in any format

    Returns:
        Clean short URL or None if invalid
    """
    video_id = extract_video_id(url)
    if video_id:
        return f"https://youtu.be/{video_id}"
    return None


def get_cache_path(video_id: str, cache_dir: str = ".youtube") -> Path:
    """
    Get the cache file path for a video ID.

    Args:
        video_id: YouTube video ID
        cache_dir: Cache directory name (default: .youtube)

    Returns:
        Path object for the cache file
    """
    cache_path = Path.cwd() / cache_dir
    cache_path.mkdir(exist_ok=True)
    return cache_path / f"{video_id}.json"


def read_cache(video_id: str, cache_dir: str = ".youtube") -> dict | None:
    """
    Read transcript from cache if available.

    Args:
        video_id: YouTube video ID
        cache_dir: Cache directory name (default: .youtube)

    Returns:
        Cached transcript data or None if not found
    """
    cache_file = get_cache_path(video_id, cache_dir)
    if cache_file.exists():
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    return None


def write_cache(video_id: str, data: dict, cache_dir: str = ".youtube") -> bool:
    """
    Write transcript data to cache.

    Expected data format:
    {
        "video_id": "abc123",
        "title": "Video Title",
        "transcript": [...]  # Can be empty list if no transcript available
    }

    Args:
        video_id: YouTube video ID
        data: Transcript data to cache
        cache_dir: Cache directory name (default: .youtube)

    Returns:
        True if successful, False otherwise
    """
    cache_file = get_cache_path(video_id, cache_dir)
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False


def create_cache_entry(video_id: str, title: str = "", transcript: list = None) -> dict:
    """
    Create a standardized cache entry.

    Args:
        video_id: YouTube video ID
        title: Video title (optional)
        transcript: Transcript data (optional, defaults to empty list)

    Returns:
        Standardized cache entry dictionary
    """
    return {
        "video_id": video_id,
        "title": title,
        "transcript": transcript if transcript is not None else []
    }


def has_transcript(data: dict | None) -> bool:
    """
    Check if cached data contains a valid transcript.

    Args:
        data: Cached data dictionary

    Returns:
        True if transcript exists and is not empty
    """
    return (
        data is not None
        and isinstance(data, dict)
        and "transcript" in data
        and isinstance(data["transcript"], list)
        and len(data["transcript"]) > 0
    )


def main():
    """Example usage of the utilities."""
    # Test URLs
    test_urls = [
        "https://www.youtube.com/watch?v=eIoohUmYpGI&feature=share",
        "https://youtu.be/eIoohUmYpGI?si=xyz123",
        "https://m.youtube.com/watch?v=eIoohUmYpGI",
        "https://www.youtube.com/embed/eIoohUmYpGI",
    ]

    print("Testing URL cleaning:")
    for url in test_urls:
        clean_url = clean_youtube_url(url)
        print(f"  {url}\n  -> {clean_url}\n")


if __name__ == "__main__":
    main()
