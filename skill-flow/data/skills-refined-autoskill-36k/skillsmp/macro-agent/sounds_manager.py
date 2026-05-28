#!/usr/bin/env python3
"""
Sound Manager for macro-agent skill
Provides audio feedback for actions (click, scroll, type, etc.)
Can be globally enabled/disabled without affecting sequence execution.
State is persisted to file so it works across processes.
"""

import os
import time
import random
import threading
import json
from pathlib import Path

# Sound directory
SOUNDS_DIR = Path(__file__).parent / "sounds"
STATE_FILE = Path(__file__).parent / "data" / "sounds_state.json"

# Global state (loaded from file on first access)
_sounds_enabled = None  # None means not loaded yet
_volume = 0.5
_last_sound_time = 0
_min_interval = 0.05  # 50ms minimum between sounds

# Sound libraries (lazy loaded)
_sd = None
_sf = None
_libs_loaded = False
_libs_available = False


def _load_state():
    """Load state from file"""
    global _sounds_enabled, _volume
    if _sounds_enabled is not None:
        return  # Already loaded
    
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
                _sounds_enabled = state.get('enabled', False)
                _volume = state.get('volume', 0.5)
        except:
            _sounds_enabled = False
            _volume = 0.5
    else:
        _sounds_enabled = False
        _volume = 0.5


def _save_state():
    """Save state to file"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump({'enabled': _sounds_enabled, 'volume': _volume}, f)


def _load_libs():
    """Lazy load sound libraries"""
    global _sd, _sf, _libs_loaded, _libs_available
    if _libs_loaded:
        return _libs_available
    
    _libs_loaded = True
    try:
        import sounddevice as sd
        import soundfile as sf
        _sd = sd
        _sf = sf
        _libs_available = True
    except ImportError:
        _libs_available = False
        print("[sounds] Warning: sounddevice/soundfile not installed. Run: pip install sounddevice soundfile")
    
    return _libs_available


def _play_sound_file(filename: str, volume: float = None):
    """Play a sound file in a separate thread (non-blocking)"""
    global _last_sound_time
    
    # Load state on first access
    _load_state()
    
    if not _sounds_enabled:
        return
    
    if not _load_libs():
        return
    
    # Rate limiting
    current_time = time.time()
    if current_time - _last_sound_time < _min_interval:
        return
    _last_sound_time = current_time
    
    # Find sound file
    sound_path = SOUNDS_DIR / filename
    if not sound_path.exists():
        # Try with extensions
        for ext in ['.wav', '.mp3']:
            test_path = SOUNDS_DIR / f"{filename}{ext}"
            if test_path.exists():
                sound_path = test_path
                break
        else:
            return
    
    vol = volume if volume is not None else _volume
    
    # Play sound synchronously (no thread) so it completes before process exits
    try:
        data, samplerate = _sf.read(str(sound_path))
        data = data * vol
        _sd.play(data, samplerate)
        # Don't wait - let it play in background but at least it started
    except Exception:
        pass


# ============================================================
# PUBLIC API - Enable/Disable
# ============================================================

def enable_sounds():
    """Enable sound feedback globally"""
    global _sounds_enabled
    _load_state()
    _sounds_enabled = True
    _save_state()
    sound_success()  # Confirmation sound
    return "🔊 Sounds enabled"


def disable_sounds():
    """Disable sound feedback globally"""
    global _sounds_enabled
    _load_state()
    _sounds_enabled = False
    _save_state()
    return "🔇 Sounds disabled"


def sounds_enabled() -> bool:
    """Check if sounds are enabled"""
    _load_state()
    return _sounds_enabled


def set_volume(vol: float):
    """Set volume (0.0 to 1.0)"""
    global _volume
    _load_state()
    _volume = max(0.0, min(1.0, vol))
    _save_state()
    return f"🔊 Volume set to {int(_volume * 100)}%"


def get_status() -> dict:
    """Get current sound status"""
    _load_state()
    return {
        "enabled": _sounds_enabled,
        "volume": _volume,
        "sounds_dir": str(SOUNDS_DIR),
        "libs_available": _load_libs()
    }


# ============================================================
# SOUND FUNCTIONS - Called by macro actions
# ============================================================

def sound_click():
    """Play click sound"""
    _play_sound_file("click.wav")


def sound_double_click():
    """Play double-click sound"""
    _play_sound_file("doubleclick.wav")


def sound_move():
    """Play mouse move sound"""
    _play_sound_file("move.wav")


def sound_scroll():
    """Play scroll sound"""
    _play_sound_file("scroll.wav")


def sound_type(text_length: int = 0):
    """Play typing sound based on text length"""
    if text_length == 0:
        _play_sound_file("singlekeypress.wav")
    elif text_length < 10:
        short_sounds = ["type_1_short.wav", "type_2_short.wav", "type_3_short.wav", "type_4_short.wav"]
        _play_sound_file(random.choice(short_sounds))
    else:
        long_sounds = ["type_5_long.wav", "type_6_long.wav", "type_7_long.wav", "type_8_long.wav"]
        _play_sound_file(random.choice(long_sounds))


def sound_key():
    """Play single key press sound"""
    _play_sound_file("singlekeypress.wav")


def sound_hotkey():
    """Play hotkey sound"""
    _play_sound_file("singlekeypress.wav")


def sound_success():
    """Play success sound"""
    _play_sound_file("success.wav")


def sound_error():
    """Play error sound"""
    _play_sound_file("error.wav")


def sound_wait():
    """Play waiting sound"""
    _play_sound_file("wait.wav")


def sound_screenshot():
    """Play screenshot sound"""
    _play_sound_file("screenshot.wav")


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    print("Testing sound manager...")
    print(f"Sounds dir: {SOUNDS_DIR}")
    print(f"Libs available: {_load_libs()}")
    
    enable_sounds()
    print("Playing test sounds...")
    
    sound_click()
    time.sleep(0.3)
    sound_success()
    time.sleep(1)
    
    print("Done!")
