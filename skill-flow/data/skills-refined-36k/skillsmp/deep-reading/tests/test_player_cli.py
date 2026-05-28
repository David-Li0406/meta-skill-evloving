"""Tests for player/cli.py"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, call
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestGetSource:
    """Tests for get_source function"""

    def test_get_source_found(self, monkeypatch, temp_dir):
        """Test get_source returns source data"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('player') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db, get_connection
        init_db()

        # Insert test data
        conn = get_connection()
        conn.execute("""
            INSERT INTO sources (id, type, url, title, author, duration, cache_path, processing_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("test123", "youtube", "http://test", "Test Title", "Test Author", 300, "/tmp/cache", "ready"))
        conn.commit()
        conn.close()

        from player.cli import get_source

        result = get_source("test123")
        assert result["id"] == "test123"
        assert result["title"] == "Test Title"

    def test_get_source_not_found(self, monkeypatch, temp_dir):
        """Test get_source raises ValueError when not found"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('player') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db
        init_db()

        from player.cli import get_source

        with pytest.raises(ValueError, match="Source not found"):
            get_source("nonexistent")


class TestListSources:
    """Tests for list_sources function"""

    def test_list_sources_empty(self, monkeypatch, temp_dir, capsys):
        """Test list_sources with no sources"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('player') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db
        init_db()

        from player.cli import list_sources

        list_sources()

        captured = capsys.readouterr()
        assert "No sources found" in captured.out

    def test_list_sources_with_data(self, monkeypatch, temp_dir, capsys):
        """Test list_sources displays sources"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('player') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db, get_connection
        init_db()

        conn = get_connection()
        conn.execute("""
            INSERT INTO sources (id, type, url, title, author, duration, cache_path, processing_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("test123", "youtube", "http://test", "Test Video", "Test Author", 300, "/tmp", "ready"))
        conn.commit()
        conn.close()

        from player.cli import list_sources

        list_sources()

        captured = capsys.readouterr()
        assert "test123" in captured.out
        assert "Test Video" in captured.out
        assert "Test Author" in captured.out
        assert "5:00" in captured.out  # 300 seconds

    def test_list_sources_no_duration(self, monkeypatch, temp_dir, capsys):
        """Test list_sources handles null duration"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('player') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db, get_connection
        init_db()

        conn = get_connection()
        conn.execute("""
            INSERT INTO sources (id, type, url, title, author, duration, cache_path, processing_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("test123", "youtube", "http://test", "Test Video", "Test Author", None, "/tmp", "ready"))
        conn.commit()
        conn.close()

        from player.cli import list_sources

        list_sources()

        captured = capsys.readouterr()
        assert "?" in captured.out  # Unknown duration


class TestPlay:
    """Tests for play function"""

    def test_play_audio_not_found(self, monkeypatch, temp_dir, capsys):
        """Test play exits when audio file not found"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('player') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db, get_connection
        init_db()

        cache_path = temp_dir / "cache"
        cache_path.mkdir(parents=True, exist_ok=True)

        conn = get_connection()
        conn.execute("""
            INSERT INTO sources (id, type, url, title, author, duration, cache_path, processing_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("test123", "youtube", "http://test", "Test", "Author", 300, str(cache_path), "ready"))
        conn.commit()
        conn.close()

        from player.cli import play

        with pytest.raises(SystemExit) as exc_info:
            play("test123")

        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Audio file not found" in captured.out

    def test_play_interactive_quit(self, monkeypatch, temp_dir, capsys):
        """Test play with quit key pressed"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('player') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db, get_connection
        init_db()

        cache_path = temp_dir / "cache"
        cache_path.mkdir(parents=True, exist_ok=True)
        (cache_path / "audio.mp3").write_text("fake audio")

        conn = get_connection()
        conn.execute("""
            INSERT INTO sources (id, type, url, title, author, duration, cache_path, processing_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("test123", "youtube", "http://test", "Test Video", "Test Author", 300, str(cache_path), "ready"))
        conn.commit()
        conn.close()

        # Mock terminal functions
        mock_mpv = MagicMock()
        mock_mpv.get_position.return_value = 10.0
        mock_mpv.get_duration.return_value = 300.0
        mock_mpv.get_speed.return_value = 1.0
        mock_mpv.get_paused.return_value = False

        mock_stdin = MagicMock()
        mock_stdin.fileno.return_value = 0
        mock_stdin.read.return_value = 'q'

        with patch('player.cli.MpvController', return_value=mock_mpv):
            with patch('tty.setraw'):
                with patch('termios.tcgetattr', return_value=[]):
                    with patch('termios.tcsetattr'):
                        with patch('select.select', return_value=([mock_stdin], [], [])):
                            with patch('sys.stdin', mock_stdin):
                                from player.cli import play
                                play("test123")

        captured = capsys.readouterr()
        assert "Playing: Test Video" in captured.out
        assert "Playback ended" in captured.out
        mock_mpv.stop.assert_called_once()

    def test_play_interactive_controls(self, monkeypatch, temp_dir, capsys):
        """Test play with various control keys"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('player') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db, get_connection
        init_db()

        cache_path = temp_dir / "cache"
        cache_path.mkdir(parents=True, exist_ok=True)
        (cache_path / "audio.mp3").write_text("fake audio")

        conn = get_connection()
        conn.execute("""
            INSERT INTO sources (id, type, url, title, author, duration, cache_path, processing_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("test123", "youtube", "http://test", "Test", "Author", 300, str(cache_path), "ready"))
        conn.commit()
        conn.close()

        mock_mpv = MagicMock()
        mock_mpv.get_position.return_value = 10.0
        mock_mpv.get_duration.return_value = 300.0
        mock_mpv.get_speed.return_value = 1.0
        mock_mpv.get_paused.return_value = True  # Test paused state

        mock_stdin = MagicMock()
        mock_stdin.fileno.return_value = 0
        # Simulate pressing space, +, -, j, k, J, K, =, then q
        mock_stdin.read.side_effect = [' ', '+', '-', 'j', 'k', 'J', 'K', '=', 'q']

        call_count = [0]
        def mock_select(*args):
            call_count[0] += 1
            if call_count[0] <= 9:
                return ([mock_stdin], [], [])
            return ([], [], [])

        with patch('player.cli.MpvController', return_value=mock_mpv):
            with patch('tty.setraw'):
                with patch('termios.tcgetattr', return_value=[]):
                    with patch('termios.tcsetattr'):
                        with patch('select.select', side_effect=mock_select):
                            with patch('sys.stdin', mock_stdin):
                                from player.cli import play
                                play("test123")

        # Verify controls were called
        mock_mpv.toggle_pause.assert_called()
        assert mock_mpv.speed_up.call_count == 2  # + and =
        mock_mpv.speed_down.assert_called_once()
        assert mock_mpv.seek.call_count == 4  # j, k, J, K

    def test_play_ends_naturally(self, monkeypatch, temp_dir, capsys):
        """Test play ends when playback completes"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('player') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db, get_connection
        init_db()

        cache_path = temp_dir / "cache"
        cache_path.mkdir(parents=True, exist_ok=True)
        (cache_path / "audio.mp3").write_text("fake audio")

        conn = get_connection()
        conn.execute("""
            INSERT INTO sources (id, type, url, title, author, duration, cache_path, processing_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("test123", "youtube", "http://test", "Test", "Author", 100, str(cache_path), "ready"))
        conn.commit()
        conn.close()

        mock_mpv = MagicMock()
        # Simulate playback ending - position >= duration - 0.5
        mock_mpv.get_position.return_value = 99.6
        mock_mpv.get_duration.return_value = 100.0
        mock_mpv.get_speed.return_value = 1.0
        mock_mpv.get_paused.return_value = False

        mock_stdin = MagicMock()
        mock_stdin.fileno.return_value = 0

        with patch('player.cli.MpvController', return_value=mock_mpv):
            with patch('tty.setraw'):
                with patch('termios.tcgetattr', return_value=[]):
                    with patch('termios.tcsetattr'):
                        with patch('select.select', return_value=([], [], [])):
                            with patch('sys.stdin', mock_stdin):
                                from player.cli import play
                                play("test123")

        captured = capsys.readouterr()
        assert "Playback ended" in captured.out

    def test_play_zero_duration_progress(self, monkeypatch, temp_dir, capsys):
        """Test play handles zero duration gracefully"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('player') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db, get_connection
        init_db()

        cache_path = temp_dir / "cache"
        cache_path.mkdir(parents=True, exist_ok=True)
        (cache_path / "audio.mp3").write_text("fake audio")

        conn = get_connection()
        conn.execute("""
            INSERT INTO sources (id, type, url, title, author, duration, cache_path, processing_state)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("test123", "youtube", "http://test", "Test", "Author", 100, str(cache_path), "ready"))
        conn.commit()
        conn.close()

        mock_mpv = MagicMock()
        mock_mpv.get_position.return_value = 0.0
        mock_mpv.get_duration.return_value = 0.0  # Zero duration
        mock_mpv.get_speed.return_value = 1.0
        mock_mpv.get_paused.return_value = False

        mock_stdin = MagicMock()
        mock_stdin.fileno.return_value = 0
        mock_stdin.read.return_value = 'q'

        with patch('player.cli.MpvController', return_value=mock_mpv):
            with patch('tty.setraw'):
                with patch('termios.tcgetattr', return_value=[]):
                    with patch('termios.tcsetattr'):
                        with patch('select.select', return_value=([mock_stdin], [], [])):
                            with patch('sys.stdin', mock_stdin):
                                from player.cli import play
                                play("test123")

        # Should handle zero duration without division by zero
        captured = capsys.readouterr()
        assert "Playback ended" in captured.out


class TestMain:
    """Tests for main function"""

    def test_main_list_flag(self, monkeypatch, temp_dir):
        """Test main with --list flag calls list_sources"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('player') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db
        init_db()

        from player import cli as player_cli

        mock_list = MagicMock()
        player_cli.list_sources = mock_list

        with patch('sys.argv', ['cli.py', '-l']):
            player_cli.main()

        mock_list.assert_called_once()

    def test_main_no_args_calls_list(self, monkeypatch, temp_dir):
        """Test main with no args calls list_sources"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('player') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db
        init_db()

        from player import cli as player_cli

        mock_list = MagicMock()
        player_cli.list_sources = mock_list

        with patch('sys.argv', ['cli.py']):
            player_cli.main()

        mock_list.assert_called_once()

    def test_main_with_source_id_calls_play(self, monkeypatch, temp_dir):
        """Test main with source_id calls play"""
        mock_config = MagicMock()
        mock_config.DB_PATH = temp_dir / "db" / "test.db"
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        (temp_dir / "db").mkdir(parents=True, exist_ok=True)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        for mod in list(sys.modules.keys()):
            if mod.startswith('player') or mod in ['db', 'models']:
                del sys.modules[mod]

        from db import init_db
        init_db()

        from player import cli as player_cli

        mock_play = MagicMock()
        player_cli.play = mock_play

        with patch('sys.argv', ['cli.py', 'test_source_id']):
            player_cli.main()

        mock_play.assert_called_once_with('test_source_id')
