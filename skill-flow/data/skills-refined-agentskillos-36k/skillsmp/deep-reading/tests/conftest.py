"""Pytest configuration and fixtures"""
import pytest
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import MagicMock, patch
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config(temp_dir, monkeypatch):
    """Mock config module with temporary paths"""
    config_module = MagicMock()
    config_module.HOME = temp_dir
    config_module.DEEP_READING_DIR = temp_dir / ".deep-reading"
    config_module.CACHE_DIR = temp_dir / ".deep-reading" / "cache"
    config_module.DB_PATH = temp_dir / ".deep-reading" / "db" / "deep_reading.db"
    config_module.LOG_DIR = temp_dir / ".deep-reading" / "logs"
    config_module.OBSIDIAN_VAULT = temp_dir / "smart notes"
    config_module.OBSIDIAN_DEEP_READING = temp_dir / "smart notes" / "DeepReading"
    config_module.OBSIDIAN_SOURCES = temp_dir / "smart notes" / "DeepReading" / "Sources"
    config_module.OBSIDIAN_CARDS = temp_dir / "smart notes" / "DeepReading" / "Cards"
    config_module.DEFAULT_SPEED = 1.0
    config_module.MPV_SOCKET = str(temp_dir / "mpv.sock")
    config_module.AUTO_PROCESS = True
    config_module.CARD_MIN_IMPORTANCE = 0.7
    config_module.VOICE_BACKEND = "macos"
    config_module.WHISPER_MODEL = "base"

    # Create directories
    config_module.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    config_module.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    config_module.OBSIDIAN_SOURCES.mkdir(parents=True, exist_ok=True)

    # Patch sys.modules
    monkeypatch.setitem(sys.modules, 'config', config_module)

    return config_module


@pytest.fixture
def test_db(mock_config):
    """Create a test database"""
    from db import init_db, get_connection

    # Re-import to pick up mocked config
    import importlib
    import db
    importlib.reload(db)

    db.init_db()
    return db


@pytest.fixture
def sample_source_data():
    """Sample source data for testing"""
    return {
        "id": "youtube_test123",
        "type": "youtube",
        "url": "https://www.youtube.com/watch?v=test123",
        "title": "Test Video Title",
        "author": "Test Author",
        "duration": 300,
        "cache_path": "/tmp/test_cache",
        "processing_state": "ready"
    }


@pytest.fixture
def sample_metadata():
    """Sample YouTube metadata"""
    return {
        "id": "test123",
        "title": "Test Video Title",
        "author": "Test Author",
        "duration": 300,
        "url": "https://www.youtube.com/watch?v=test123",
        "description": "Test description",
        "upload_date": "20260121",
    }


@pytest.fixture
def sample_vtt_content():
    """Sample VTT subtitle content"""
    return """WEBVTT
Kind: captions
Language: en

00:00:00.000 --> 00:00:02.000 align:start position:0%
Hello world

00:00:02.000 --> 00:00:04.000 align:start position:0%
This is a test

00:00:04.000 --> 00:00:06.000 align:start position:0%
Hello world

00:00:06.000 --> 00:00:08.000 align:start position:0%
<c>Formatted</c> text here
"""


@pytest.fixture
def mock_subprocess():
    """Mock subprocess for external commands"""
    with patch('subprocess.run') as mock_run, \
         patch('subprocess.Popen') as mock_popen:
        yield {"run": mock_run, "popen": mock_popen}
