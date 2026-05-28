"""Tests for processor/cli.py"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestProcessSource:
    """Tests for process_source function"""

    def test_process_source_not_found(self, monkeypatch, temp_dir, capsys):
        """Test process_source exits when source not found"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.OBSIDIAN_SOURCES = temp_dir / "Sources"
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('processor') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db
        init_db()

        from processor.cli import process_source

        with pytest.raises(SystemExit) as exc_info:
            process_source("nonexistent")

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Source not found" in captured.out

    def test_process_source_success(self, monkeypatch, temp_dir, capsys):
        """Test process_source generates report successfully"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.OBSIDIAN_SOURCES = temp_dir / "Sources"
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('processor') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db, get_connection
        init_db()

        # Create cache with transcript
        cache_path = temp_dir / "cache"
        cache_path.mkdir(parents=True, exist_ok=True)
        (cache_path / "transcript.txt").write_text("This is the transcript")

        conn = get_connection()
        conn.execute("""
            INSERT INTO sources (id, type, url, title, author, duration, cache_path, processing_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("test123", "youtube", "http://test", "Test Video", "Test Author", 300, str(cache_path), "ready"))
        conn.commit()
        conn.close()

        from processor.cli import process_source

        process_source("test123")

        captured = capsys.readouterr()
        assert "Generating inspectional report" in captured.out
        assert "Report saved to" in captured.out

        # Check report was created
        assert (temp_dir / "Sources").exists()
        report_files = list((temp_dir / "Sources").glob("*.md"))
        assert len(report_files) == 1

    def test_process_source_no_transcript(self, monkeypatch, temp_dir, capsys):
        """Test process_source handles missing transcript"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.OBSIDIAN_SOURCES = temp_dir / "Sources"
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('processor') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db, get_connection
        init_db()

        # Create cache without transcript
        cache_path = temp_dir / "cache"
        cache_path.mkdir(parents=True, exist_ok=True)

        conn = get_connection()
        conn.execute("""
            INSERT INTO sources (id, type, url, title, author, duration, cache_path, processing_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("test123", "youtube", "http://test", "Test Video", "Test Author", 300, str(cache_path), "ready"))
        conn.commit()
        conn.close()

        from processor.cli import process_source

        # Should not raise, just use empty transcript
        process_source("test123")

        captured = capsys.readouterr()
        assert "Report saved to" in captured.out

    def test_process_source_saves_to_database(self, monkeypatch, temp_dir):
        """Test process_source saves note to database"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.OBSIDIAN_SOURCES = temp_dir / "Sources"
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('processor') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db, get_connection
        init_db()

        cache_path = temp_dir / "cache"
        cache_path.mkdir(parents=True, exist_ok=True)

        conn = get_connection()
        conn.execute("""
            INSERT INTO sources (id, type, url, title, author, duration, cache_path, processing_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("test123", "youtube", "http://test", "Test Video", "Test Author", 300, str(cache_path), "ready"))
        conn.commit()
        conn.close()

        from processor.cli import process_source

        process_source("test123")

        # Check note was saved to database
        conn = get_connection()
        row = conn.execute("SELECT * FROM notes WHERE source_id = ?", ("test123",)).fetchone()
        conn.close()

        assert row is not None
        assert row["type"] == "source"
        assert row["title"] == "Test Video"
        assert row["status"] == "draft"


class TestMain:
    """Tests for main function"""

    def test_main_parses_source_id(self, monkeypatch, temp_dir):
        """Test main parses source_id argument"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.OBSIDIAN_SOURCES = temp_dir / "Sources"
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('processor') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db
        init_db()

        from processor import cli as processor_cli

        mock_process = MagicMock()
        processor_cli.process_source = mock_process

        with patch('sys.argv', ['cli.py', 'youtube_test123']):
            processor_cli.main()

        mock_process.assert_called_once_with('youtube_test123')
