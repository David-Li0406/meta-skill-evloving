# Deep Reading v2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a CLI-based deep reading system with TUI audio player and Obsidian integration for knowledge management.

**Architecture:** CLI tools (Bash + Python) for content fetching and control, mpv for background audio playback, TUI for interactive player interface, Obsidian vault for note storage with bi-directional linking.

**Tech Stack:** Bash, Python 3.11+, yt-dlp, mpv, Textual (TUI), SQLite, Obsidian Markdown

---

## Milestone Overview

| Milestone | Description | Tasks |
|-----------|-------------|-------|
| **M1** | 基础可用：YouTube 下载 + 简单播放 + 检视阅读 | 1-6 |
| **M2** | 播放体验：TUI Player + 字幕同步 | 7-11 |
| **M3** | AI 集成：章节分割 + 概念卡片 | 12-16 |
| **M4** | Obsidian：笔记写入 + 双链 + 审核 | 17-21 |
| **M5** | 播客支持 | 22-24 |
| **M6** | 网页支持 | 25-27 |

---

## M1: 基础可用 (YouTube + 播放 + 检视阅读)

### Task 1: 项目结构初始化

**Files:**
- Create: `~/.deep-reading/` (运行时目录)
- Create: `src/` (Python 源码)
- Create: `bin/dr` (主入口脚本)
- Modify: `config.sh` → 新配置格式

**Step 1: 创建目录结构**

```bash
mkdir -p ~/.deep-reading/{cache,db,logs}
mkdir -p src/{fetcher,player,processor,notes}
mkdir -p bin
touch src/__init__.py
touch src/fetcher/__init__.py
touch src/player/__init__.py
touch src/processor/__init__.py
touch src/notes/__init__.py
```

**Step 2: 创建主入口脚本**

Create `bin/dr`:
```bash
#!/bin/bash
# Deep Reading CLI
# Usage: dr <command> [args]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_PATH="$SCRIPT_DIR/src"

export PYTHONPATH="$PYTHON_PATH:$PYTHONPATH"

case "${1:-help}" in
    fetch|f)
        shift
        python3 -m fetcher.cli "$@"
        ;;
    play|p)
        shift
        python3 -m player.cli "$@"
        ;;
    review|r)
        shift
        python3 -m notes.cli "$@"
        ;;
    status|s)
        python3 -m fetcher.status "$@"
        ;;
    *)
        echo "Deep Reading v2"
        echo ""
        echo "Usage: dr <command> [args]"
        echo ""
        echo "Commands:"
        echo "  fetch, f <url>    Download and process content"
        echo "  play, p [id]      Play content in TUI player"
        echo "  review, r         Review and sync notes to Obsidian"
        echo "  status, s         Show processing status"
        ;;
esac
```

**Step 3: 让脚本可执行**

```bash
chmod +x bin/dr
```

**Step 4: 创建新配置文件**

Create `~/.deep-reading/config.py`:
```python
"""Deep Reading Configuration"""
from pathlib import Path

# Paths
HOME = Path.home()
DEEP_READING_DIR = HOME / ".deep-reading"
CACHE_DIR = DEEP_READING_DIR / "cache"
DB_PATH = DEEP_READING_DIR / "db" / "deep_reading.db"
LOG_DIR = DEEP_READING_DIR / "logs"

# Obsidian
OBSIDIAN_VAULT = HOME / "smart notes"
OBSIDIAN_DEEP_READING = OBSIDIAN_VAULT / "DeepReading"
OBSIDIAN_SOURCES = OBSIDIAN_DEEP_READING / "Sources"
OBSIDIAN_CARDS = OBSIDIAN_DEEP_READING / "Cards"

# Player
DEFAULT_SPEED = 1.0
MPV_SOCKET = "/tmp/deep-reading-mpv.sock"

# AI
AUTO_PROCESS = True
CARD_MIN_IMPORTANCE = 0.7

# Voice
VOICE_BACKEND = "macos"  # macos | whisper
WHISPER_MODEL = "base"
```

**Step 5: Commit**

```bash
git add bin/ src/
git commit -m "feat: initialize project structure for v2

- Add bin/dr CLI entry point
- Create src/ Python package structure
- Add runtime config at ~/.deep-reading/"
```

---

### Task 2: SQLite 数据库 Schema

**Files:**
- Create: `src/db.py`
- Create: `src/models.py`

**Step 1: 创建数据库模块**

Create `src/db.py`:
```python
"""Database connection and initialization"""
import sqlite3
from pathlib import Path

# Import config
import sys
sys.path.insert(0, str(Path.home() / ".deep-reading"))
from config import DB_PATH

def get_connection() -> sqlite3.Connection:
    """Get database connection with row factory"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database schema"""
    conn = get_connection()
    conn.executescript("""
        -- Content sources
        CREATE TABLE IF NOT EXISTS sources (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            url TEXT,
            title TEXT,
            author TEXT,
            duration INTEGER,
            cache_path TEXT,
            processing_state TEXT DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        -- Chapters (semantic segments)
        CREATE TABLE IF NOT EXISTS chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT NOT NULL,
            start_time INTEGER NOT NULL,
            end_time INTEGER NOT NULL,
            title TEXT,
            type TEXT DEFAULT 'core',
            FOREIGN KEY (source_id) REFERENCES sources(id)
        );

        -- User marks during playback
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT NOT NULL,
            timestamp INTEGER NOT NULL,
            type TEXT NOT NULL,
            content TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_id) REFERENCES sources(id)
        );

        -- Generated notes
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_id TEXT,
            type TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT,
            obsidian_path TEXT,
            status TEXT DEFAULT 'draft',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_id) REFERENCES sources(id)
        );

        -- Note links
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_note_id INTEGER NOT NULL,
            to_note_id INTEGER NOT NULL,
            type TEXT DEFAULT 'auto',
            status TEXT DEFAULT 'pending',
            FOREIGN KEY (from_note_id) REFERENCES notes(id),
            FOREIGN KEY (to_note_id) REFERENCES notes(id)
        );

        -- Indexes
        CREATE INDEX IF NOT EXISTS idx_sources_state ON sources(processing_state);
        CREATE INDEX IF NOT EXISTS idx_chapters_source ON chapters(source_id);
        CREATE INDEX IF NOT EXISTS idx_marks_source ON marks(source_id);
        CREATE INDEX IF NOT EXISTS idx_notes_source ON notes(source_id);
        CREATE INDEX IF NOT EXISTS idx_notes_status ON notes(status);
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
```

**Step 2: 测试数据库初始化**

```bash
python3 src/db.py
# Expected: Database initialized at /Users/liweixin/.deep-reading/db/deep_reading.db
```

**Step 3: 创建数据模型**

Create `src/models.py`:
```python
"""Data models for Deep Reading"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class SourceType(Enum):
    YOUTUBE = "youtube"
    PODCAST = "podcast"
    WEB = "web"
    PDF = "pdf"

class ProcessingState(Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PROCESSING = "processing"
    READY = "ready"
    REVIEWED = "reviewed"
    ERROR = "error"

class ChapterType(Enum):
    INTRO = "intro"
    CORE = "core"
    SKIP = "skip"
    OUTRO = "outro"

class MarkType(Enum):
    HIGHLIGHT = "highlight"
    QUESTION = "question"
    NOTE = "note"

class NoteType(Enum):
    SOURCE = "source"
    CARD = "card"

class NoteStatus(Enum):
    DRAFT = "draft"
    REVIEWED = "reviewed"
    SYNCED = "synced"

@dataclass
class Source:
    id: str
    type: SourceType
    url: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    duration: Optional[int] = None  # seconds
    cache_path: Optional[str] = None
    processing_state: ProcessingState = ProcessingState.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class Chapter:
    id: Optional[int]
    source_id: str
    start_time: int  # seconds
    end_time: int    # seconds
    title: str
    type: ChapterType = ChapterType.CORE

@dataclass
class Mark:
    id: Optional[int]
    source_id: str
    timestamp: int  # seconds
    type: MarkType
    content: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class Note:
    id: Optional[int]
    source_id: Optional[str]
    type: NoteType
    title: str
    content: Optional[str] = None
    obsidian_path: Optional[str] = None
    status: NoteStatus = NoteStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
```

**Step 4: Commit**

```bash
git add src/db.py src/models.py
git commit -m "feat: add SQLite database schema and data models

- Initialize DB with sources, chapters, marks, notes, links tables
- Add dataclass models with enums for type safety"
```

---

### Task 3: YouTube 内容下载器

**Files:**
- Create: `src/fetcher/youtube.py`
- Create: `src/fetcher/cli.py`

**Step 1: 创建 YouTube 下载模块**

Create `src/fetcher/youtube.py`:
```python
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
```

**Step 2: 测试 YouTube 下载**

```bash
python3 -c "
from src.fetcher.youtube import fetch_youtube
result = fetch_youtube('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
print(result)
"
```

**Step 3: 创建 CLI 入口**

Create `src/fetcher/cli.py`:
```python
"""Fetcher CLI"""
import sys
import argparse
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path.home() / ".deep-reading"))

from fetcher.youtube import fetch_youtube, extract_video_id
from db import get_connection, init_db
from models import SourceType, ProcessingState

def detect_source_type(url: str) -> str:
    """Detect source type from URL"""
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif url.endswith(".mp3") or "podcast" in url.lower():
        return "podcast"
    else:
        return "web"

def fetch(url: str):
    """Fetch content from URL"""
    init_db()

    source_type = detect_source_type(url)
    print(f"Detected source type: {source_type}")

    if source_type == "youtube":
        result = fetch_youtube(url)

        # Save to database
        conn = get_connection()
        conn.execute("""
            INSERT OR REPLACE INTO sources
            (id, type, url, title, author, duration, cache_path, processing_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result["id"],
            source_type,
            url,
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
        print(f"\nTo play: dr play {result['id']}")

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
```

**Step 4: 测试 CLI**

```bash
python3 -m src.fetcher.cli "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Step 5: Commit**

```bash
git add src/fetcher/
git commit -m "feat: add YouTube content fetcher

- Download audio (mp3), transcript (vtt + txt), metadata (json)
- Clean VTT to plain text with deduplication
- Save to SQLite database
- CLI: dr fetch <url>"
```

---

### Task 4: mpv 播放控制

**Files:**
- Create: `src/player/mpv_controller.py`

**Step 1: 创建 mpv 控制器**

Create `src/player/mpv_controller.py`:
```python
"""mpv IPC controller for audio playback"""
import socket
import json
import subprocess
import time
from pathlib import Path
from typing import Optional
import sys

sys.path.insert(0, str(Path.home() / ".deep-reading"))
from config import MPV_SOCKET

class MpvController:
    """Control mpv player via IPC socket"""

    def __init__(self, socket_path: str = MPV_SOCKET):
        self.socket_path = socket_path
        self.process: Optional[subprocess.Popen] = None
        self.sock: Optional[socket.socket] = None

    def start(self, audio_path: str):
        """Start mpv with the given audio file"""
        # Kill any existing mpv
        self.stop()

        # Remove old socket
        socket_file = Path(self.socket_path)
        if socket_file.exists():
            socket_file.unlink()

        # Start mpv in background
        self.process = subprocess.Popen([
            "mpv",
            "--no-video",
            "--no-terminal",
            f"--input-ipc-server={self.socket_path}",
            "--idle=yes",
            audio_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Wait for socket
        for _ in range(50):  # 5 seconds timeout
            if socket_file.exists():
                break
            time.sleep(0.1)
        else:
            raise Exception("mpv socket not created")

        # Connect
        self._connect()

    def _connect(self):
        """Connect to mpv socket"""
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.socket_path)
        self.sock.setblocking(False)

    def _send_command(self, command: list) -> Optional[dict]:
        """Send command to mpv and get response"""
        if not self.sock:
            return None

        msg = json.dumps({"command": command}) + "\n"
        self.sock.send(msg.encode())

        # Read response
        time.sleep(0.05)
        try:
            data = self.sock.recv(4096).decode()
            for line in data.strip().split("\n"):
                if line:
                    return json.loads(line)
        except BlockingIOError:
            pass
        return None

    def _get_property(self, name: str):
        """Get mpv property value"""
        result = self._send_command(["get_property", name])
        if result and "data" in result:
            return result["data"]
        return None

    def _set_property(self, name: str, value):
        """Set mpv property value"""
        self._send_command(["set_property", name, value])

    # Playback control
    def play(self):
        """Resume playback"""
        self._set_property("pause", False)

    def pause(self):
        """Pause playback"""
        self._set_property("pause", True)

    def toggle_pause(self):
        """Toggle pause state"""
        current = self._get_property("pause")
        self._set_property("pause", not current)
        return not current

    def seek(self, seconds: float, mode: str = "relative"):
        """Seek to position
        mode: 'relative', 'absolute', 'absolute-percent'
        """
        self._send_command(["seek", seconds, mode])

    def seek_to(self, seconds: float):
        """Seek to absolute position"""
        self.seek(seconds, "absolute")

    # Playback info
    def get_position(self) -> float:
        """Get current playback position in seconds"""
        return self._get_property("time-pos") or 0.0

    def get_duration(self) -> float:
        """Get total duration in seconds"""
        return self._get_property("duration") or 0.0

    def get_paused(self) -> bool:
        """Check if paused"""
        return self._get_property("pause") or False

    # Speed control
    def get_speed(self) -> float:
        """Get playback speed"""
        return self._get_property("speed") or 1.0

    def set_speed(self, speed: float):
        """Set playback speed (0.5 - 3.0)"""
        speed = max(0.5, min(3.0, speed))
        self._set_property("speed", speed)

    def speed_up(self, delta: float = 0.25):
        """Increase speed"""
        current = self.get_speed()
        self.set_speed(current + delta)

    def speed_down(self, delta: float = 0.25):
        """Decrease speed"""
        current = self.get_speed()
        self.set_speed(current - delta)

    # Cleanup
    def stop(self):
        """Stop mpv and cleanup"""
        if self.sock:
            try:
                self._send_command(["quit"])
                self.sock.close()
            except:
                pass
            self.sock = None

        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except:
                self.process.kill()
            self.process = None

        # Remove socket file
        socket_file = Path(self.socket_path)
        if socket_file.exists():
            socket_file.unlink()

    def __del__(self):
        self.stop()


def format_time(seconds: float) -> str:
    """Format seconds as HH:MM:SS or MM:SS"""
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


# Simple test
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python mpv_controller.py <audio_file>")
        sys.exit(1)

    mpv = MpvController()
    mpv.start(sys.argv[1])

    print("Controls: [space] pause, [q] quit, [+/-] speed")

    import tty
    import termios

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        while True:
            pos = mpv.get_position()
            dur = mpv.get_duration()
            speed = mpv.get_speed()
            paused = "⏸" if mpv.get_paused() else "▶"

            status = f"\r{paused} {format_time(pos)} / {format_time(dur)} [{speed:.2f}x]   "
            sys.stdout.write(status)
            sys.stdout.flush()

            # Check for input
            import select
            if select.select([sys.stdin], [], [], 0.1)[0]:
                ch = sys.stdin.read(1)
                if ch == 'q':
                    break
                elif ch == ' ':
                    mpv.toggle_pause()
                elif ch == '+' or ch == '=':
                    mpv.speed_up()
                elif ch == '-':
                    mpv.speed_down()
                elif ch == 'j':
                    mpv.seek(10)
                elif ch == 'k':
                    mpv.seek(-10)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        mpv.stop()
        print("\nDone")
```

**Step 2: 测试 mpv 控制器**

```bash
# First download a test file
python3 -m src.fetcher.cli "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Then test playback
python3 src/player/mpv_controller.py ~/.deep-reading/cache/youtube/dQw4w9WgXcQ/audio.mp3
```

**Step 3: Commit**

```bash
git add src/player/
git commit -m "feat: add mpv IPC controller for audio playback

- Start/stop mpv with IPC socket
- Play, pause, seek, speed control
- Get position, duration, status
- Simple terminal test interface"
```

---

### Task 5: 简单播放 CLI

**Files:**
- Create: `src/player/cli.py`

**Step 1: 创建播放 CLI**

Create `src/player/cli.py`:
```python
"""Simple player CLI"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path.home() / ".deep-reading"))

from player.mpv_controller import MpvController, format_time
from db import get_connection

def get_source(source_id: str) -> dict:
    """Get source from database"""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM sources WHERE id = ?",
        (source_id,)
    ).fetchone()
    conn.close()

    if not row:
        raise ValueError(f"Source not found: {source_id}")

    return dict(row)

def list_sources():
    """List all available sources"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, title, author, duration, processing_state FROM sources ORDER BY created_at DESC"
    ).fetchall()
    conn.close()

    if not rows:
        print("No sources found. Use 'dr fetch <url>' to add content.")
        return

    print("Available sources:\n")
    for row in rows:
        duration = format_time(row["duration"]) if row["duration"] else "?"
        state = row["processing_state"]
        print(f"  [{row['id']}]")
        print(f"    {row['title']}")
        print(f"    by {row['author']} | {duration} | {state}")
        print()

def play(source_id: str):
    """Play a source"""
    source = get_source(source_id)
    cache_path = Path(source["cache_path"])
    audio_path = cache_path / "audio.mp3"

    if not audio_path.exists():
        print(f"Audio file not found: {audio_path}")
        sys.exit(1)

    print(f"Playing: {source['title']}")
    print(f"By: {source['author']}")
    print()
    print("Controls: [space] pause, [j/k] seek, [+/-] speed, [q] quit")
    print()

    mpv = MpvController()
    mpv.start(str(audio_path))

    import tty
    import termios
    import select

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        while True:
            pos = mpv.get_position()
            dur = mpv.get_duration()
            speed = mpv.get_speed()
            paused = "⏸" if mpv.get_paused() else "▶"

            # Progress bar
            progress = pos / dur if dur > 0 else 0
            bar_width = 30
            filled = int(bar_width * progress)
            bar = "━" * filled + "●" + "─" * (bar_width - filled - 1)

            status = f"\r  {paused} {bar} {format_time(pos)} / {format_time(dur)} [{speed:.1f}x]   "
            sys.stdout.write(status)
            sys.stdout.flush()

            # Check for input
            if select.select([sys.stdin], [], [], 0.1)[0]:
                ch = sys.stdin.read(1)
                if ch == 'q':
                    break
                elif ch == ' ':
                    mpv.toggle_pause()
                elif ch == '+' or ch == '=':
                    mpv.speed_up()
                elif ch == '-':
                    mpv.speed_down()
                elif ch == 'j':
                    mpv.seek(30)
                elif ch == 'k':
                    mpv.seek(-10)
                elif ch == 'J':
                    mpv.seek(60)
                elif ch == 'K':
                    mpv.seek(-30)

            # Check if playback ended
            if pos >= dur - 0.5 and dur > 0:
                break

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        mpv.stop()
        print("\n\nPlayback ended.")

def main():
    parser = argparse.ArgumentParser(description="Play content")
    parser.add_argument("source_id", nargs="?", help="Source ID to play")
    parser.add_argument("-l", "--list", action="store_true", help="List sources")
    args = parser.parse_args()

    if args.list or not args.source_id:
        list_sources()
    else:
        play(args.source_id)

if __name__ == "__main__":
    main()
```

**Step 2: 测试播放**

```bash
# List sources
python3 -m src.player.cli -l

# Play
python3 -m src.player.cli youtube_dQw4w9WgXcQ
```

**Step 3: Commit**

```bash
git add src/player/cli.py
git commit -m "feat: add simple player CLI

- List available sources
- Play with keyboard controls
- Progress bar display
- Speed control"
```

---

### Task 6: 检视阅读生成

**Files:**
- Create: `src/processor/inspectional.py`
- Create: `src/processor/cli.py`

**Step 1: 创建检视阅读处理器**

Create `src/processor/inspectional.py`:
```python
"""Inspectional reading report generator"""
import json
from pathlib import Path
from datetime import datetime
from typing import Optional
import sys

sys.path.insert(0, str(Path.home() / ".deep-reading"))
from config import OBSIDIAN_SOURCES

def generate_inspectional_report(
    source_id: str,
    title: str,
    author: str,
    url: str,
    duration: int,
    transcript: str,
    ai_analysis: Optional[dict] = None
) -> str:
    """Generate inspectional reading report in Markdown"""

    date_str = datetime.now().strftime("%Y-%m-%d")
    duration_str = f"{duration // 3600}:{(duration % 3600) // 60:02d}:{duration % 60:02d}"

    # If no AI analysis provided, create placeholder
    if not ai_analysis:
        ai_analysis = {
            "summary": "待 AI 分析生成",
            "key_points": ["待分析"],
            "concepts": [],
            "questions": [],
        }

    report = f"""---
source_type: youtube
source_id: {source_id}
source_url: {url}
title: "{title}"
author: "{author}"
duration: "{duration_str}"
date_consumed: {date_str}
tags: []
status: draft
---

# {title}

## 元信息
- **来源**: [YouTube]({url})
- **作者**: {author}
- **时长**: {duration_str}
- **阅读日期**: {date_str}

## 快速摘要

{ai_analysis.get('summary', '待 AI 分析...')}

## 核心观点

"""

    for i, point in enumerate(ai_analysis.get('key_points', []), 1):
        report += f"{i}. {point}\n"

    report += """
## 关键概念

"""

    for concept in ai_analysis.get('concepts', []):
        report += f"- [[{concept}]]\n"

    report += """
## 我的标记

> 播放时添加的标记会显示在这里

## 我的笔记

> 听后感想...

## 思考问题

"""

    for q in ai_analysis.get('questions', []):
        report += f"- {q}\n"

    report += """
## 相关来源

> 相关内容链接...
"""

    return report

def save_report(source_id: str, title: str, content: str) -> Path:
    """Save report to Obsidian vault"""
    OBSIDIAN_SOURCES.mkdir(parents=True, exist_ok=True)

    # Clean title for filename
    safe_title = "".join(c for c in title if c.isalnum() or c in " -_").strip()
    safe_title = safe_title[:100]  # Limit length

    file_path = OBSIDIAN_SOURCES / f"{safe_title}.md"

    with open(file_path, "w") as f:
        f.write(content)

    return file_path
```

**Step 2: 创建处理器 CLI**

Create `src/processor/cli.py`:
```python
"""Processor CLI - generate reading reports"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path.home() / ".deep-reading"))

from processor.inspectional import generate_inspectional_report, save_report
from db import get_connection

def process_source(source_id: str):
    """Process a source and generate inspectional report"""
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM sources WHERE id = ?",
        (source_id,)
    ).fetchone()

    if not row:
        print(f"Source not found: {source_id}")
        sys.exit(1)

    source = dict(row)
    cache_path = Path(source["cache_path"])
    transcript_path = cache_path / "transcript.txt"

    # Read transcript
    transcript = ""
    if transcript_path.exists():
        transcript = transcript_path.read_text()

    print(f"Generating inspectional report for: {source['title']}")

    # Generate report (without AI for now)
    report = generate_inspectional_report(
        source_id=source_id,
        title=source["title"],
        author=source["author"],
        url=source["url"],
        duration=source["duration"],
        transcript=transcript,
    )

    # Save to Obsidian
    file_path = save_report(source_id, source["title"], report)

    # Update database
    conn.execute("""
        INSERT OR REPLACE INTO notes (source_id, type, title, obsidian_path, status)
        VALUES (?, 'source', ?, ?, 'draft')
    """, (source_id, source["title"], str(file_path)))
    conn.commit()
    conn.close()

    print(f"✓ Report saved to: {file_path}")
    print(f"\nOpen in Obsidian to review and edit.")

def main():
    parser = argparse.ArgumentParser(description="Process content")
    parser.add_argument("source_id", help="Source ID to process")
    args = parser.parse_args()

    process_source(args.source_id)

if __name__ == "__main__":
    main()
```

**Step 3: 测试报告生成**

```bash
python3 -m src.processor.cli youtube_dQw4w9WgXcQ

# Check the generated file
ls -la "/Users/liweixin/smart notes/DeepReading/Sources/"
```

**Step 4: Commit**

```bash
git add src/processor/
git commit -m "feat: add inspectional reading report generator

- Generate Markdown report with frontmatter
- Save to Obsidian vault
- Placeholder for AI analysis
- Track in database"
```

---

## M1 Complete Checkpoint

At this point, M1 is complete. The system can:
1. ✅ Download YouTube content (audio + transcript + metadata)
2. ✅ Play audio with keyboard controls
3. ✅ Generate basic inspectional reading report
4. ✅ Save to Obsidian vault

**Test the full workflow:**

```bash
# 1. Fetch content
./bin/dr fetch "https://www.youtube.com/watch?v=RSNuB9pj9P8"

# 2. List sources
./bin/dr play -l

# 3. Play
./bin/dr play youtube_RSNuB9pj9P8

# 4. Generate report (in another terminal or after playback)
python3 -m src.processor.cli youtube_RSNuB9pj9P8

# 5. Open Obsidian and check the note
```

---

## M2-M6 Summary (后续里程碑概要)

### M2: TUI 播放体验 (Tasks 7-11)
- Task 7: Textual TUI 框架搭建
- Task 8: 字幕同步显示
- Task 9: 章节导航
- Task 10: 用户标记功能 (m 键)
- Task 11: 语音笔记 (v 键)

### M3: AI 集成 (Tasks 12-16)
- Task 12: Claude API 集成
- Task 13: 语义章节分割
- Task 14: 干货识别
- Task 15: 概念卡片提取
- Task 16: 双链关系识别

### M4: Obsidian 集成 (Tasks 17-21)
- Task 17: 笔记模板系统
- Task 18: 审核 TUI 界面
- Task 19: 双链自动创建
- Task 20: 增量同步
- Task 21: 已有笔记关联

### M5: 播客支持 (Tasks 22-24)
- Task 22: RSS 解析器
- Task 23: 播客元数据提取
- Task 24: Show notes 集成

### M6: 网页支持 (Tasks 25-27)
- Task 25: Readability 集成
- Task 26: 网页内容清洗
- Task 27: 阅读模式

---

**Plan complete and saved to `docs/plans/2026-01-21-deep-reading-v2.md`.**

**Two execution options:**

1. **Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

2. **Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**
