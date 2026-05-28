#!/usr/bin/env python3
"""
Save YouTube transcript directly to Bookmarks database.

This script fetches a YouTube transcript and writes it to Database/Bookmarks
with the filename pattern: youtube-{video_id}.md

The Database/Bookmarks directory acts as a cache - if a video already has a
bookmark file with a valid transcript, it won't be re-fetched.

This avoids polluting chat context with full transcript content.
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime


def extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from URL."""
    import re
    from urllib.parse import urlparse, parse_qs

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
        elif parsed.path.startswith('/embed/'):
            return parsed.path.split('/')[2]
        elif parsed.path.startswith('/v/'):
            return parsed.path.split('/')[2]

    return None


def clean_youtube_url(url: str) -> str | None:
    """Convert any YouTube URL to clean short form."""
    video_id = extract_video_id(url)
    if video_id:
        return f"https://youtu.be/{video_id}"
    return None


def concatenate_transcript(transcript_data: list) -> str:
    """
    Concatenate transcript segments into continuous text.

    Args:
        transcript_data: List of transcript segments with 'text' field

    Returns:
        Concatenated transcript text
    """
    if not transcript_data:
        return ""

    return " ".join(segment.get("text", "") for segment in transcript_data)


def create_bookmark_content(video_id: str, url: str, title: str, transcript_text: str) -> str:
    """
    Create bookmark markdown content for YouTube video.

    Args:
        video_id: YouTube video ID
        url: Clean YouTube URL
        title: Video title
        transcript_text: Concatenated transcript text

    Returns:
        Formatted bookmark markdown content
    """
    today = datetime.now().strftime("%Y-%m-%d")

    # Escape any special characters in title for YAML frontmatter
    safe_title = title.replace('"', '\\"')

    content = f"""---
type: bookmark
url: {url}
category: Video
tags:
  - bookmark
  - youtube
  - video
description: YouTube video transcript
saved: true
rating:
created: {today}
last_accessed: {today}
---

# {title}

## URL

[Visit]({url})

## Description

YouTube video transcript.

## Transcript

{transcript_text}

## Key Takeaways

-

## Related

Links to related bookmarks, projects, or notes.

## Notes

Additional notes, quotes, or highlights.

---

*Created: {today}*
*Last accessed: {today}*
"""

    return content


def check_existing_bookmark(video_id: str, bookmarks_dir: str = "Database/Bookmarks") -> dict | None:
    """
    Check if a bookmark file already exists for this video ID.

    Args:
        video_id: YouTube video ID
        bookmarks_dir: Path to Bookmarks directory

    Returns:
        Dictionary with 'exists', 'filepath', and 'has_transcript' keys, or None on error
    """
    script_dir = Path(__file__).resolve().parent
    # Go up from scripts/ -> youtube/ -> skills/ -> .claude/ -> workspace_root
    workspace_root = script_dir.parent.parent.parent.parent
    bookmarks_path = workspace_root / bookmarks_dir

    filename = f"youtube-{video_id}.md"
    filepath = bookmarks_path / filename

    if not filepath.exists():
        return {"exists": False, "filepath": str(filepath), "has_transcript": False}

    # Check if the file contains a valid transcript (not empty/failed)
    try:
        content = filepath.read_text(encoding='utf-8')

        # Check for failure indicators
        has_failed = (
            "No transcript available" in content
            or "## Transcript\n\n-" in content  # Empty key takeaway
            or "## Transcript\n\n\n" in content  # Empty transcript section
        )

        # Check if transcript section has substantial content
        transcript_match = re.search(r'## Transcript\n\n(.+?)\n\n## Key Takeaways', content, re.DOTALL)
        has_content = transcript_match and len(transcript_match.group(1).strip()) > 50

        return {
            "exists": True,
            "filepath": str(filepath.relative_to(workspace_root)),
            "has_transcript": has_content and not has_failed
        }
    except Exception:
        return {"exists": True, "filepath": str(filepath), "has_transcript": False}


def save_to_bookmarks(video_id: str, url: str, title: str, transcript_text: str, bookmarks_dir: str = "Database/Bookmarks") -> Path:
    """
    Save transcript to Bookmarks database.

    Args:
        video_id: YouTube video ID
        url: Clean YouTube URL
        title: Video title
        transcript_text: Concatenated transcript text
        bookmarks_dir: Path to Bookmarks directory

    Returns:
        Path to created bookmark file
    """
    # Get workspace root (go up from .claude/skills/youtube/scripts to workspace root)
    script_dir = Path(__file__).resolve().parent
    # Go up from scripts/ -> youtube/ -> skills/ -> .claude/ -> workspace_root
    workspace_root = script_dir.parent.parent.parent.parent

    bookmarks_path = workspace_root / bookmarks_dir
    bookmarks_path.mkdir(parents=True, exist_ok=True)

    filename = f"youtube-{video_id}.md"
    filepath = bookmarks_path / filename

    content = create_bookmark_content(video_id, url, title, transcript_text)

    filepath.write_text(content, encoding='utf-8')

    return filepath


def main():
    """
    Main entry point for saving transcript to bookmarks.

    Expected input (stdin JSON):
    {
        "url": "https://youtube.com/watch?v=...",
        "title": "Video Title",
        "transcript": [{"text": "...", "start": 0.0, "duration": 1.5}, ...],
        "force": false  // Optional: force re-fetch even if cached
    }

    Output (stdout JSON):
    {
        "success": true,
        "video_id": "abc123",
        "filepath": "Database/Bookmarks/youtube-abc123.md",
        "url": "https://youtu.be/abc123",
        "cached": false  // True if existing valid transcript was found
    }
    """
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)

        url = input_data.get("url")
        title = input_data.get("title", "Untitled Video")
        transcript_data = input_data.get("transcript", [])
        force = input_data.get("force", False)

        if not url:
            print(json.dumps({
                "success": False,
                "error": "No URL provided"
            }))
            sys.exit(1)

        # Extract video ID and clean URL
        video_id = extract_video_id(url)
        if not video_id:
            print(json.dumps({
                "success": False,
                "error": "Invalid YouTube URL"
            }))
            sys.exit(1)

        clean_url = clean_youtube_url(url)

        # Check if already cached (unless force flag is set)
        if not force:
            existing = check_existing_bookmark(video_id)
            if existing and existing["exists"] and existing["has_transcript"]:
                # Valid transcript already exists, return cached result
                result = {
                    "success": True,
                    "video_id": video_id,
                    "filepath": existing["filepath"],
                    "url": clean_url,
                    "title": title,
                    "cached": True
                }
                print(json.dumps(result, indent=2))
                sys.exit(0)

        # Concatenate transcript
        transcript_text = concatenate_transcript(transcript_data)

        if not transcript_text:
            transcript_text = "No transcript available for this video."

        # Save to bookmarks
        filepath = save_to_bookmarks(video_id, clean_url, title, transcript_text)

        # Output success result
        result = {
            "success": True,
            "video_id": video_id,
            "filepath": str(filepath.relative_to(filepath.parent.parent.parent)),
            "url": clean_url,
            "title": title,
            "cached": False
        }

        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({
            "success": False,
            "error": "Invalid JSON input"
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
