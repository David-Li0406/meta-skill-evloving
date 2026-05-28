"""Tests for fetcher/cli.py"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestDetectSourceType:
    """Tests for detect_source_type function"""

    def test_detect_youtube_standard(self, monkeypatch, temp_dir):
        """Test detecting YouTube from standard URL"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in ['fetcher.cli', 'fetcher.youtube', 'db', 'models']:
            if mod in sys.modules:
                del sys.modules[mod]

        from fetcher.cli import detect_source_type

        assert detect_source_type("https://www.youtube.com/watch?v=test") == "youtube"

    def test_detect_youtube_short(self, monkeypatch, temp_dir):
        """Test detecting YouTube from youtu.be URL"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in ['fetcher.cli', 'fetcher.youtube', 'db', 'models']:
            if mod in sys.modules:
                del sys.modules[mod]

        from fetcher.cli import detect_source_type

        assert detect_source_type("https://youtu.be/test") == "youtube"

    def test_detect_podcast_mp3(self, monkeypatch, temp_dir):
        """Test detecting podcast from mp3 URL"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in ['fetcher.cli', 'fetcher.youtube', 'db', 'models']:
            if mod in sys.modules:
                del sys.modules[mod]

        from fetcher.cli import detect_source_type

        assert detect_source_type("https://example.com/episode.mp3") == "podcast"

    def test_detect_podcast_keyword(self, monkeypatch, temp_dir):
        """Test detecting podcast from URL with podcast keyword"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in ['fetcher.cli', 'fetcher.youtube', 'db', 'models']:
            if mod in sys.modules:
                del sys.modules[mod]

        from fetcher.cli import detect_source_type

        assert detect_source_type("https://podcasts.example.com/show") == "podcast"

    def test_detect_web_default(self, monkeypatch, temp_dir):
        """Test that unknown URLs default to web"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in ['fetcher.cli', 'fetcher.youtube', 'db', 'models']:
            if mod in sys.modules:
                del sys.modules[mod]

        from fetcher.cli import detect_source_type

        assert detect_source_type("https://example.com/article") == "web"


class TestFetch:
    """Tests for fetch function"""

    def test_fetch_youtube_success(self, monkeypatch, temp_dir, capsys):
        """Test successful YouTube fetch"""
        # Setup mock config
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        # Clear modules
        for mod in list(sys.modules.keys()):
            if mod.startswith('fetcher') or mod in ['db', 'models']:
                del sys.modules[mod]

        # Mock fetch_youtube
        mock_fetch_youtube = MagicMock(return_value={
            "id": "youtube_test123",
            "type": "youtube",
            "video_id": "test123",
            "metadata": {
                "title": "Test Video",
                "author": "Test Author",
                "duration": 300
            },
            "cache_dir": str(temp_dir / "cache" / "youtube" / "test123")
        })

        with patch.dict('sys.modules', {'fetcher.youtube': MagicMock(
                fetch_youtube=mock_fetch_youtube,
                extract_video_id=MagicMock(return_value="test123")
        )}):
            from fetcher.cli import fetch
            from db import init_db
            init_db()

            fetch("https://www.youtube.com/watch?v=test123")

        captured = capsys.readouterr()
        assert "Downloaded: Test Video" in captured.out
        assert "youtube_test123" in captured.out

    def test_fetch_unsupported_type_exits(self, monkeypatch, temp_dir, capsys):
        """Test that unsupported source type exits with error"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('fetcher') or mod in ['db', 'models']:
                del sys.modules[mod]

        from fetcher.cli import fetch
        from db import init_db
        init_db()

        with pytest.raises(SystemExit) as exc_info:
            fetch("https://example.com/article")

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "not yet implemented" in captured.out


class TestMain:
    """Tests for main function"""

    def test_main_parses_url(self, monkeypatch, temp_dir):
        """Test that main parses URL argument"""
        mock_config = MagicMock()
        mock_config.CACHE_DIR = temp_dir / "cache"
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('fetcher') or mod in ['db', 'models']:
                del sys.modules[mod]

        from fetcher import cli as fetcher_cli

        mock_fetch = MagicMock()
        fetcher_cli.fetch = mock_fetch

        with patch('sys.argv', ['cli.py', 'https://youtube.com/watch?v=test']):
            fetcher_cli.main()

        mock_fetch.assert_called_once_with('https://youtube.com/watch?v=test')
