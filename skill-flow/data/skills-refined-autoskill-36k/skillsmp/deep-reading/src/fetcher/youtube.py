"""YouTube content fetcher using yt-dlp"""
import subprocess
import json
import re
from pathlib import Path
from typing import Optional, Tuple
import sys

sys.path.insert(0, str(Path.home() / ".deep-reading"))
from config import CACHE_DIR

def extract_video_id(url: str) -> Optional[str]:
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'youtu\.be/([a-zA-Z0-9_-]+)',
        r'youtube\.com.*[?&]v=([a-zA-Z0-9_-]+)',
        r'youtube\.com/shorts/([a-zA-Z0-9_-]+)',
        r'youtube\.com/embed/([a-zA-Z0-9_-]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1).split('&')[0].split('?')[0]
    return None

def get_cache_dir(video_id: str) -> Path:
    """Get cache directory for a video"""
    cache_dir = CACHE_DIR / "youtube" / video_id
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

def fetch_metadata(url: str, video_id: str) -> dict:
    """Fetch video metadata using yt-dlp"""
    result = subprocess.run(
        ["yt-dlp", "--dump-json", "--no-download", url],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"Failed to fetch metadata: {result.stderr}")

    data = json.loads(result.stdout)

    metadata = {
        "id": video_id,
        "title": data.get("title", "Unknown"),
        "author": data.get("channel", data.get("uploader", "Unknown")),
        "duration": data.get("duration", 0),
        "url": url,
        "description": data.get("description", ""),
        "upload_date": data.get("upload_date", ""),
    }

    # Save to cache
    cache_dir = get_cache_dir(video_id)
    with open(cache_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return metadata

def fetch_audio(url: str, video_id: str) -> Path:
    """Download audio as mp3"""
    cache_dir = get_cache_dir(video_id)
    audio_path = cache_dir / "audio.mp3"

    if audio_path.exists():
        print(f"Audio already cached: {audio_path}")
        return audio_path

    print("Downloading audio...")
    result = subprocess.run([
        "yt-dlp",
        "-x",  # Extract audio
        "--audio-format", "mp3",
        "--audio-quality", "0",  # Best quality
        "-o", str(audio_path),
        url
    ], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"Failed to download audio: {result.stderr}")

    # yt-dlp may add extension, find the actual file
    if not audio_path.exists():
        for f in cache_dir.glob("audio.*"):
            if f.suffix in [".mp3", ".m4a", ".opus", ".webm"]:
                f.rename(audio_path)
                break

    return audio_path

def fetch_transcript(url: str, video_id: str) -> Tuple[Path, Path]:
    """Download subtitles/transcript"""
    cache_dir = get_cache_dir(video_id)
    vtt_path = cache_dir / "transcript.vtt"
    txt_path = cache_dir / "transcript.txt"

    if txt_path.exists():
        print(f"Transcript already cached: {txt_path}")
        return vtt_path, txt_path

    print("Downloading transcript...")

    # Try auto-generated subtitles first
    result = subprocess.run([
        "yt-dlp",
        "--skip-download",
        "--write-auto-sub",
        "--sub-lang", "en",
        "--sub-format", "vtt",
        "-o", str(cache_dir / "transcript"),
        url
    ], capture_output=True, text=True)

    # Find the downloaded vtt file
    vtt_files = list(cache_dir.glob("transcript*.vtt"))
    if not vtt_files:
        # Try manual subtitles
        result = subprocess.run([
            "yt-dlp",
            "--skip-download",
            "--write-subs",
            "--sub-lang", "en",
            "--sub-format", "vtt",
            "-o", str(cache_dir / "transcript"),
            url
        ], capture_output=True, text=True)
        vtt_files = list(cache_dir.glob("transcript*.vtt"))

    if not vtt_files:
        raise Exception("No subtitles available for this video")

    # Rename to standard name
    vtt_files[0].rename(vtt_path)

    # Clean VTT to plain text
    clean_transcript(vtt_path, txt_path)

    return vtt_path, txt_path

def clean_transcript(vtt_path: Path, txt_path: Path):
    """Clean VTT file to plain text"""
    with open(vtt_path, "r") as f:
        content = f.read()

    # Remove VTT headers and timestamps
    lines = content.split("\n")
    cleaned = []
    seen = set()

    for line in lines:
        # Skip headers
        if line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        # Skip timestamps
        if re.match(r'^\d{2}:\d{2}:\d{2}', line):
            continue
        # Skip empty lines and alignment tags
        if not line.strip() or "align:" in line:
            continue
        # Remove HTML tags
        line = re.sub(r'<[^>]+>', '', line)
        # Deduplicate
        if line not in seen:
            seen.add(line)
            cleaned.append(line)

    with open(txt_path, "w") as f:
        f.write("\n".join(cleaned))

def fetch_youtube(url: str) -> dict:
    """Main entry point: fetch all content from YouTube URL"""
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError(f"Could not extract video ID from URL: {url}")

    print(f"Fetching YouTube video: {video_id}")

    # Fetch all components
    metadata = fetch_metadata(url, video_id)
    audio_path = fetch_audio(url, video_id)
    vtt_path, txt_path = fetch_transcript(url, video_id)

    cache_dir = get_cache_dir(video_id)

    return {
        "id": f"youtube_{video_id}",
        "type": "youtube",
        "video_id": video_id,
        "metadata": metadata,
        "cache_dir": str(cache_dir),
        "audio_path": str(audio_path),
        "vtt_path": str(vtt_path),
        "txt_path": str(txt_path),
    }
