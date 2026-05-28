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
