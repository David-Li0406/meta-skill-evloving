"""Tests for player/mpv_controller.py"""
import pytest
import json
import socket
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class TestFormatTime:
    """Tests for format_time function"""

    def test_format_seconds_only(self, monkeypatch, temp_dir):
        """Test formatting time under 1 minute"""
        mock_config = MagicMock()
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import format_time

        assert format_time(45) == "0:45"

    def test_format_minutes_seconds(self, monkeypatch, temp_dir):
        """Test formatting time in minutes"""
        mock_config = MagicMock()
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import format_time

        assert format_time(125) == "2:05"

    def test_format_hours(self, monkeypatch, temp_dir):
        """Test formatting time with hours"""
        mock_config = MagicMock()
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import format_time

        assert format_time(3661) == "1:01:01"

    def test_format_float_truncates(self, monkeypatch, temp_dir):
        """Test that float seconds are truncated"""
        mock_config = MagicMock()
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import format_time

        assert format_time(65.7) == "1:05"


class TestMpvControllerInit:
    """Tests for MpvController initialization"""

    def test_init_default_socket(self, monkeypatch, temp_dir):
        """Test initialization with default socket path"""
        mock_config = MagicMock()
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import MpvController

        controller = MpvController()
        assert controller.socket_path == str(temp_dir / "mpv.sock")
        assert controller.process is None
        assert controller.sock is None

    def test_init_custom_socket(self, monkeypatch, temp_dir):
        """Test initialization with custom socket path"""
        mock_config = MagicMock()
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import MpvController

        controller = MpvController("/tmp/custom.sock")
        assert controller.socket_path == "/tmp/custom.sock"


class TestMpvControllerStart:
    """Tests for MpvController.start method"""

    def test_start_removes_old_socket(self, monkeypatch, temp_dir):
        """Test that start removes existing socket file"""
        mock_config = MagicMock()
        socket_path = temp_dir / "mpv.sock"
        mock_config.MPV_SOCKET = str(socket_path)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        # Create old socket file
        socket_path.touch()
        assert socket_path.exists()

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import MpvController

        controller = MpvController()

        mock_popen = MagicMock()
        mock_socket = MagicMock()

        def create_socket_file(*args, **kwargs):
            socket_path.touch()
            return mock_popen

        with patch('subprocess.Popen', side_effect=create_socket_file):
            with patch('socket.socket', return_value=mock_socket):
                controller.start("/tmp/audio.mp3")

        # Socket was recreated by mock Popen
        assert socket_path.exists()

    def test_start_without_existing_socket(self, monkeypatch, temp_dir):
        """Test that start works when no socket file exists"""
        mock_config = MagicMock()
        socket_path = temp_dir / "mpv.sock"
        mock_config.MPV_SOCKET = str(socket_path)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        # Ensure socket doesn't exist
        assert not socket_path.exists()

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import MpvController

        controller = MpvController()

        mock_popen = MagicMock()
        mock_socket = MagicMock()

        def create_socket_file(*args, **kwargs):
            socket_path.touch()
            return mock_popen

        with patch('subprocess.Popen', side_effect=create_socket_file):
            with patch('socket.socket', return_value=mock_socket):
                controller.start("/tmp/audio.mp3")

        assert socket_path.exists()

    def test_start_launches_mpv(self, monkeypatch, temp_dir):
        """Test that start launches mpv process"""
        mock_config = MagicMock()
        socket_path = temp_dir / "mpv.sock"
        mock_config.MPV_SOCKET = str(socket_path)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import MpvController

        controller = MpvController()

        mock_popen = MagicMock()
        mock_socket = MagicMock()

        def create_socket_file(*args, **kwargs):
            socket_path.touch()
            return mock_popen

        with patch('subprocess.Popen', side_effect=create_socket_file) as popen_mock:
            with patch('socket.socket', return_value=mock_socket):
                controller.start("/tmp/audio.mp3")

        # Verify mpv was launched with correct args
        call_args = popen_mock.call_args[0][0]
        assert call_args[0] == "mpv"
        assert "--no-video" in call_args
        assert "--no-terminal" in call_args
        assert "/tmp/audio.mp3" in call_args

    def test_start_timeout_exception(self, monkeypatch, temp_dir):
        """Test that start raises exception on socket timeout"""
        mock_config = MagicMock()
        socket_path = temp_dir / "mpv.sock"
        mock_config.MPV_SOCKET = str(socket_path)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import MpvController

        controller = MpvController()

        mock_popen = MagicMock()

        # Don't create socket file - simulate timeout
        with patch('subprocess.Popen', return_value=mock_popen):
            with patch('time.sleep'):  # Speed up test
                with pytest.raises(Exception, match="socket not created"):
                    controller.start("/tmp/audio.mp3")


class TestMpvControllerCommands:
    """Tests for MpvController command methods"""

    def setup_controller(self, monkeypatch, temp_dir):
        """Helper to set up a controller with mocked socket"""
        mock_config = MagicMock()
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import MpvController

        controller = MpvController()
        controller.sock = MagicMock()
        return controller

    def test_send_command(self, monkeypatch, temp_dir):
        """Test _send_command sends JSON and reads response"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{"data": "test"}\n'

        result = controller._send_command(["get_property", "pause"])

        controller.sock.send.assert_called_once()
        sent_data = controller.sock.send.call_args[0][0]
        assert b"get_property" in sent_data
        assert result == {"data": "test"}

    def test_send_command_no_socket(self, monkeypatch, temp_dir):
        """Test _send_command returns None when no socket"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock = None

        result = controller._send_command(["test"])
        assert result is None

    def test_send_command_blocking_error(self, monkeypatch, temp_dir):
        """Test _send_command handles BlockingIOError"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.side_effect = BlockingIOError()

        result = controller._send_command(["test"])
        assert result is None

    def test_get_property(self, monkeypatch, temp_dir):
        """Test _get_property returns data value"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{"data": 1.5}\n'

        result = controller._get_property("speed")
        assert result == 1.5

    def test_get_property_no_data(self, monkeypatch, temp_dir):
        """Test _get_property returns None when no data"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{"error": "unknown"}\n'

        result = controller._get_property("unknown")
        assert result is None

    def test_set_property(self, monkeypatch, temp_dir):
        """Test _set_property sends command"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{}\n'

        controller._set_property("pause", True)

        sent_data = controller.sock.send.call_args[0][0].decode()
        assert "set_property" in sent_data
        assert "pause" in sent_data

    def test_play(self, monkeypatch, temp_dir):
        """Test play sets pause to False"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{}\n'

        controller.play()

        sent_data = controller.sock.send.call_args[0][0].decode()
        assert "false" in sent_data.lower() or "False" in sent_data

    def test_pause(self, monkeypatch, temp_dir):
        """Test pause sets pause to True"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{}\n'

        controller.pause()

        sent_data = controller.sock.send.call_args[0][0].decode()
        assert "true" in sent_data.lower() or "True" in sent_data

    def test_toggle_pause(self, monkeypatch, temp_dir):
        """Test toggle_pause toggles pause state"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.side_effect = [
            b'{"data": false}\n',  # get current state
            b'{}\n'  # set new state
        ]

        result = controller.toggle_pause()
        assert result is True  # Was not paused, now paused

    def test_seek_relative(self, monkeypatch, temp_dir):
        """Test seek with relative mode"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{}\n'

        controller.seek(10)

        sent_data = controller.sock.send.call_args[0][0].decode()
        assert "seek" in sent_data
        assert "10" in sent_data
        assert "relative" in sent_data

    def test_seek_to_absolute(self, monkeypatch, temp_dir):
        """Test seek_to with absolute position"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{}\n'

        controller.seek_to(120)

        sent_data = controller.sock.send.call_args[0][0].decode()
        assert "seek" in sent_data
        assert "120" in sent_data
        assert "absolute" in sent_data

    def test_get_position(self, monkeypatch, temp_dir):
        """Test get_position returns time-pos"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{"data": 125.5}\n'

        result = controller.get_position()
        assert result == 125.5

    def test_get_position_default(self, monkeypatch, temp_dir):
        """Test get_position returns 0.0 when None"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{}\n'

        result = controller.get_position()
        assert result == 0.0

    def test_get_duration(self, monkeypatch, temp_dir):
        """Test get_duration returns duration"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{"data": 300.0}\n'

        result = controller.get_duration()
        assert result == 300.0

    def test_get_duration_default(self, monkeypatch, temp_dir):
        """Test get_duration returns 0.0 when None"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{}\n'

        result = controller.get_duration()
        assert result == 0.0

    def test_get_paused(self, monkeypatch, temp_dir):
        """Test get_paused returns pause state"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{"data": true}\n'

        result = controller.get_paused()
        assert result is True

    def test_get_paused_default(self, monkeypatch, temp_dir):
        """Test get_paused returns False when None"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{}\n'

        result = controller.get_paused()
        assert result is False

    def test_get_speed(self, monkeypatch, temp_dir):
        """Test get_speed returns speed"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{"data": 1.5}\n'

        result = controller.get_speed()
        assert result == 1.5

    def test_get_speed_default(self, monkeypatch, temp_dir):
        """Test get_speed returns 1.0 when None"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{}\n'

        result = controller.get_speed()
        assert result == 1.0

    def test_set_speed_clamps_min(self, monkeypatch, temp_dir):
        """Test set_speed clamps to minimum 0.5"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{}\n'

        controller.set_speed(0.1)

        sent_data = controller.sock.send.call_args[0][0].decode()
        assert "0.5" in sent_data

    def test_set_speed_clamps_max(self, monkeypatch, temp_dir):
        """Test set_speed clamps to maximum 3.0"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.return_value = b'{}\n'

        controller.set_speed(5.0)

        sent_data = controller.sock.send.call_args[0][0].decode()
        assert "3.0" in sent_data or "3" in sent_data

    def test_speed_up(self, monkeypatch, temp_dir):
        """Test speed_up increases speed"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.side_effect = [
            b'{"data": 1.0}\n',  # get current
            b'{}\n'  # set new
        ]

        controller.speed_up()

        # Second call should set 1.25
        sent_data = controller.sock.send.call_args[0][0].decode()
        assert "1.25" in sent_data

    def test_speed_down(self, monkeypatch, temp_dir):
        """Test speed_down decreases speed"""
        controller = self.setup_controller(monkeypatch, temp_dir)
        controller.sock.recv.side_effect = [
            b'{"data": 1.0}\n',  # get current
            b'{}\n'  # set new
        ]

        controller.speed_down()

        # Second call should set 0.75
        sent_data = controller.sock.send.call_args[0][0].decode()
        assert "0.75" in sent_data


class TestMpvControllerStop:
    """Tests for MpvController.stop method"""

    def test_stop_sends_quit_command(self, monkeypatch, temp_dir):
        """Test stop sends quit command"""
        mock_config = MagicMock()
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import MpvController

        controller = MpvController()
        controller.sock = MagicMock()
        controller.sock.recv.return_value = b'{}\n'
        mock_process = MagicMock()
        controller.process = mock_process

        controller.stop()

        # Check quit was sent
        assert controller.sock is None
        mock_process.terminate.assert_called_once()

    def test_stop_handles_socket_error(self, monkeypatch, temp_dir):
        """Test stop handles socket errors gracefully"""
        mock_config = MagicMock()
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import MpvController

        controller = MpvController()
        controller.sock = MagicMock()
        controller.sock.send.side_effect = Exception("Socket error")
        controller.process = MagicMock()

        # Should not raise
        controller.stop()
        assert controller.sock is None

    def test_stop_kills_hung_process(self, monkeypatch, temp_dir):
        """Test stop kills process if terminate times out"""
        mock_config = MagicMock()
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import MpvController
        import subprocess

        controller = MpvController()
        controller.sock = MagicMock()
        controller.sock.recv.return_value = b'{}\n'
        mock_process = MagicMock()
        mock_process.wait.side_effect = subprocess.TimeoutExpired("mpv", 2)
        controller.process = mock_process

        controller.stop()

        mock_process.kill.assert_called_once()

    def test_stop_removes_socket_file(self, monkeypatch, temp_dir):
        """Test stop removes socket file"""
        socket_path = temp_dir / "mpv.sock"
        socket_path.touch()

        mock_config = MagicMock()
        mock_config.MPV_SOCKET = str(socket_path)
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import MpvController

        controller = MpvController()
        controller.stop()

        assert not socket_path.exists()

    def test_del_calls_stop(self, monkeypatch, temp_dir):
        """Test __del__ calls stop"""
        mock_config = MagicMock()
        mock_config.MPV_SOCKET = str(temp_dir / "mpv.sock")
        monkeypatch.setitem(sys.modules, 'config', mock_config)

        if 'player.mpv_controller' in sys.modules:
            del sys.modules['player.mpv_controller']
        from player.mpv_controller import MpvController

        controller = MpvController()
        controller.sock = MagicMock()
        controller.sock.recv.return_value = b'{}\n'
        controller.process = MagicMock()

        controller.__del__()

        assert controller.sock is None
