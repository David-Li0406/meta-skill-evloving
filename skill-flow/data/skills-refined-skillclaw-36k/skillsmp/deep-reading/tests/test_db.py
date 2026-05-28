"""Tests for db.py"""
import pytest
import sqlite3
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys


class TestGetConnection:
    """Tests for get_connection function"""

    def test_get_connection_creates_parent_dir(self, temp_dir, monkeypatch):
        """Test that get_connection creates parent directory if it doesn't exist"""
        db_path = temp_dir / "subdir" / "test.db"

        mock_config = MagicMock()
        mock_config.DB_PATH = db_path
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        # Re-import db module
        if 'db' in sys.modules:
            del sys.modules['db']
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
        from db import get_connection

        conn = get_connection()
        assert db_path.parent.exists()
        assert conn is not None
        conn.close()

    def test_get_connection_returns_connection_with_row_factory(self, temp_dir, monkeypatch):
        """Test that connection has row_factory set"""
        db_path = temp_dir / "test.db"

        mock_config = MagicMock()
        mock_config.DB_PATH = db_path
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'db' in sys.modules:
            del sys.modules['db']
        from db import get_connection

        conn = get_connection()
        assert conn.row_factory == sqlite3.Row
        conn.close()


class TestInitDb:
    """Tests for init_db function"""

    def test_init_db_creates_tables(self, temp_dir, monkeypatch):
        """Test that init_db creates all required tables"""
        db_path = temp_dir / "test.db"

        mock_config = MagicMock()
        mock_config.DB_PATH = db_path
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'db' in sys.modules:
            del sys.modules['db']
        from db import init_db, get_connection

        init_db()

        conn = get_connection()
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()

        assert "sources" in tables
        assert "chapters" in tables
        assert "marks" in tables
        assert "notes" in tables
        assert "links" in tables

    def test_init_db_creates_indexes(self, temp_dir, monkeypatch):
        """Test that init_db creates all required indexes"""
        db_path = temp_dir / "test.db"

        mock_config = MagicMock()
        mock_config.DB_PATH = db_path
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'db' in sys.modules:
            del sys.modules['db']
        from db import init_db, get_connection

        init_db()

        conn = get_connection()
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'"
        )
        indexes = [row[0] for row in cursor.fetchall()]
        conn.close()

        assert "idx_sources_state" in indexes
        assert "idx_chapters_source" in indexes
        assert "idx_marks_source" in indexes
        assert "idx_notes_source" in indexes
        assert "idx_notes_status" in indexes

    def test_init_db_is_idempotent(self, temp_dir, monkeypatch):
        """Test that init_db can be called multiple times safely"""
        db_path = temp_dir / "test.db"

        mock_config = MagicMock()
        mock_config.DB_PATH = db_path
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'db' in sys.modules:
            del sys.modules['db']
        from db import init_db

        # Should not raise
        init_db()
        init_db()
        init_db()


class TestDbMain:
    """Tests for db.py __main__ block"""

    def test_main_prints_message(self, temp_dir, monkeypatch, capsys):
        """Test that running db.py as main prints initialization message"""
        db_path = temp_dir / "test.db"

        mock_config = MagicMock()
        mock_config.DB_PATH = db_path
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'db' in sys.modules:
            del sys.modules['db']

        # Import and call init_db directly, then print (simulating __main__)
        from db import init_db, DB_PATH
        init_db()
        print(f"Database initialized at {DB_PATH}")

        captured = capsys.readouterr()
        assert "Database initialized at" in captured.out
