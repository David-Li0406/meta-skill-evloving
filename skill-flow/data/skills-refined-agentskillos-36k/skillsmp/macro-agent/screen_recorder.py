#!/usr/bin/env python3
"""
Screen Recorder for macro-agent skill
Uses ffmpeg with x11grab to record the screen.
"""
import subprocess
import os
import signal
import time
from pathlib import Path
from datetime import datetime

# Recording directory
RECORDINGS_DIR = Path(__file__).parent / "data" / "recordings"
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

# Use system ffmpeg (has x11grab support)
FFMPEG_PATH = "/usr/bin/ffmpeg"

# Current recording process
_recording_process = None
_current_recording_file = None


def get_screen_resolution():
    """Get current screen resolution."""
    try:
        result = subprocess.run(
            ["xdpyinfo"], 
            capture_output=True, 
            text=True
        )
        for line in result.stdout.split('\n'):
            if 'dimensions:' in line:
                # Format: "  dimensions:    1920x1080 pixels (508x285 millimeters)"
                parts = line.split()
                if len(parts) >= 2:
                    return parts[1].split('x')  # ['1920', '1080']
    except:
        pass
    return ['1920', '1080']  # Default


def get_default_audio_monitor():
    """Get the default audio output monitor for recording system sound."""
    try:
        # Get the default sink (output device)
        result = subprocess.run(
            ["pactl", "get-default-sink"],
            capture_output=True,
            text=True
        )
        default_sink = result.stdout.strip()
        if default_sink:
            # The monitor source is sink_name.monitor
            return f"{default_sink}.monitor"
    except:
        pass
    return None


def start_recording(filename: str = None, question_id: str = None, ai_name: str = "gemini", record_audio: bool = True):
    """
    Start screen recording.
    
    Args:
        filename: Custom filename (without extension)
        question_id: ID of the question being recorded
        ai_name: Name of the AI being tested
        record_audio: If True, also record system audio
    
    Returns:
        Path to the recording file, or None if failed
    """
    global _recording_process, _current_recording_file
    
    # Stop any existing recording
    if _recording_process is not None:
        stop_recording()
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if filename:
        output_file = RECORDINGS_DIR / f"{filename}.mp4"
    elif question_id:
        output_file = RECORDINGS_DIR / f"{ai_name}_q{question_id}_{timestamp}.mp4"
    else:
        output_file = RECORDINGS_DIR / f"{ai_name}_{timestamp}.mp4"
    
    # Get screen resolution
    width, height = get_screen_resolution()
    
    # Get audio device
    audio_device = get_default_audio_monitor() if record_audio else None
    
    # Build ffmpeg command
    # Video: x11grab for screen capture
    # Audio: pulse for system audio (if available)
    cmd = [
        FFMPEG_PATH,
        '-y',
        # Video input con opciones para reducir drops
        '-video_size', f'{width}x{height}',
        '-framerate', '30',
        '-thread_queue_size', '512',  # Buffer más grande para evitar drops
        '-f', 'x11grab',
        '-draw_mouse', '1',  # Mostrar cursor
        '-i', ':0.0',
    ]
    
    # Add audio input if available
    if audio_device:
        cmd.extend([
            '-thread_queue_size', '512',  # Buffer también para audio
            '-f', 'pulse',
            '-i', audio_device,
        ])
    
    # Output options - optimizado para CPU, no GPU
    cmd.extend([
        '-c:v', 'libx264',
        '-preset', 'ultrafast',  # Más rápido para evitar drops (CPU only)
        '-crf', '23',  # Balance razonable
        '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart',  # Mejor para streaming/preview
        '-g', '60',  # Keyframe cada 2 segundos
        '-threads', '0',  # Usar todos los cores de CPU disponibles
    ])
    
    # Audio codec if recording audio
    if audio_device:
        cmd.extend([
            '-c:a', 'aac',
            '-b:a', '128k',
        ])
    
    cmd.append(str(output_file))
    
    try:
        # Start recording in background
        _recording_process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.PIPE
        )
        _current_recording_file = output_file
        print(f"🔴 Recording started: {output_file.name}")
        return str(output_file)
    
    except Exception as e:
        print(f"❌ Failed to start recording: {e}")
        return None


def stop_recording():
    """
    Stop the current screen recording.
    
    Returns:
        Path to the recorded file, or None if no recording was active
    """
    global _recording_process, _current_recording_file
    
    if _recording_process is None:
        return None
    
    output_file = _current_recording_file
    
    try:
        # Send 'q' to ffmpeg to stop gracefully
        _recording_process.stdin.write(b'q')
        _recording_process.stdin.flush()
        
        # Wait for process to finish (max 5 seconds)
        try:
            _recording_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill if it doesn't stop
            _recording_process.kill()
            _recording_process.wait()
        
        print(f"⏹️  Recording stopped: {output_file.name}")
        
    except Exception as e:
        print(f"⚠️  Error stopping recording: {e}")
        try:
            _recording_process.kill()
        except:
            pass
    
    _recording_process = None
    _current_recording_file = None
    
    return str(output_file) if output_file else None


def is_recording() -> bool:
    """Check if a recording is currently active."""
    return _recording_process is not None and _recording_process.poll() is None


def list_recordings() -> list:
    """List all recordings in the recordings directory."""
    recordings = []
    for f in RECORDINGS_DIR.glob("*.mp4"):
        recordings.append({
            "name": f.name,
            "path": str(f),
            "size_mb": f.stat().st_size / (1024 * 1024),
            "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
        })
    return sorted(recordings, key=lambda x: x['modified'], reverse=True)


# Cleanup on exit
import atexit
atexit.register(stop_recording)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: screen_recorder.py [start|stop|status|list]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "start":
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        result = start_recording(filename)
        if result:
            print(f"Recording to: {result}")
        else:
            print("Failed to start recording")
            sys.exit(1)
    
    elif cmd == "stop":
        result = stop_recording()
        if result:
            print(f"Saved: {result}")
        else:
            print("No recording was active")
    
    elif cmd == "status":
        if is_recording():
            print(f"🔴 Recording: {_current_recording_file}")
        else:
            print("⏹️  Not recording")
    
    elif cmd == "list":
        recordings = list_recordings()
        print(f"Found {len(recordings)} recordings:")
        for r in recordings:
            print(f"  {r['name']} ({r['size_mb']:.1f} MB)")
    
    elif cmd == "test":
        print("Testing screen recording for 5 seconds...")
        start_recording("test_recording")
        time.sleep(5)
        stop_recording()
        print("Done!")
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
