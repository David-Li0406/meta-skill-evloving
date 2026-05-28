"""Generate voiceover audio using Eleven Labs v3 via fal.ai."""

import json
import os
import subprocess
from pathlib import Path
from typing import Optional

import fal_client
import requests

from .utils import get_fal_key, api_call_with_retry, get_ffmpeg_path, get_ffprobe_path


# Available voices - maps name to voice ID (None means use name directly)
VOICES = {
    "George": None,      # Built-in voice
    "Aria": None,        # Built-in voice
    "Rachel": None,      # Built-in voice
    "Sam": None,         # Built-in voice
    "Charlie": None,     # Built-in voice
    "Emily": None,       # Built-in voice
    "Hope": "tnSpp4vdxKPjI9w0GnoV",  # Custom voice ID from ElevenLabs
}

# Voice descriptions for reference
VOICE_DESCRIPTIONS = {
    "George": "Professional male voice, clear and authoritative - good for business",
    "Aria": "Professional female voice, warm and engaging - good for training",
    "Rachel": "Conversational female voice - good for casual content",
    "Sam": "Young male voice, energetic - good for marketing and tech",
    "Charlie": "Neutral, authoritative voice - good for documentaries",
    "Emily": "Soft female voice, calming - good for wellness content",
    "Hope": "Natural female voice, warm and clear - good for professional narration",
}


def _resolve_voice(voice: str) -> str:
    """Resolve voice name or ID to the value to send to API.

    The fal.ai Eleven Labs API accepts both voice names and voice IDs
    in the same 'voice' parameter.

    Args:
        voice: Voice name (e.g., "George") or voice ID (e.g., "tnSpp4vdxKPjI9w0GnoV").

    Returns:
        The voice value to use in the API call (either name or ID).
    """
    # Check if it's a known voice name with a custom ID
    if voice in VOICES:
        voice_id = VOICES[voice]
        if voice_id is not None:
            return voice_id  # Use the custom voice ID
        return voice  # Use the voice name directly

    # Check if it looks like a voice ID (contains digits or is long)
    if len(voice) > 15 or any(c.isdigit() for c in voice):
        # Assume it's a custom voice ID
        return voice

    # Unknown voice name - warn and fall back to George
    print(f"Warning: Voice '{voice}' not recognized. Using 'George'.")
    return "George"


def is_valid_voice(voice: str) -> bool:
    """Check if a voice name or ID is valid.

    Args:
        voice: Voice name or voice ID.

    Returns:
        True if the voice is a known name or looks like a valid ID.
    """
    if voice in VOICES:
        return True
    # Accept any string that looks like a voice ID
    if len(voice) > 15 or any(c.isdigit() for c in voice):
        return True
    return False


def _init_fal():
    """Initialize fal client with API key."""
    os.environ["FAL_KEY"] = get_fal_key()


def generate_voiceover(
    text: str,
    slide_number: int,
    output_dir: str = "./audio",
    voice: str = "George"
) -> str:
    """Generate voiceover audio for a slide narration.

    Args:
        text: Narration script text.
        slide_number: Slide number for filename.
        output_dir: Directory to save audio files.
        voice: Voice name (George, Aria, Hope, etc.) or voice ID.

    Returns:
        Path to the generated audio file.
    """
    _init_fal()

    # Resolve voice name/ID
    voice_param = _resolve_voice(voice)

    def _generate():
        return fal_client.subscribe(
            "fal-ai/elevenlabs/tts/eleven-v3",
            arguments={
                "text": text,
                "voice": voice_param,
                "speed": 1.0,
                "output_format": "mp3_44100_128",
            },
        )

    result = api_call_with_retry(_generate)

    audio_url = result["audio"]["url"]

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"narration_{slide_number:02d}.mp3")

    response = requests.get(audio_url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


def generate_voiceover_batch(
    narrations: list[str],
    output_dir: str = "./audio",
    voice: str = "George"
) -> list[str]:
    """Generate voiceovers for all slides.

    Args:
        narrations: List of narration scripts.
        output_dir: Directory to save audio files.
        voice: Voice name to use for all narrations.

    Returns:
        List of paths to generated audio files.
    """
    paths = []
    total = len(narrations)

    for i, text in enumerate(narrations, 1):
        print(f"Generating voiceover {i}/{total}...")
        path = generate_voiceover(text, i, output_dir, voice)
        paths.append(path)
        print(f"  Saved: {path}")

    return paths


def get_voice_info(voice: Optional[str] = None) -> dict:
    """Get information about available voices.

    Args:
        voice: Specific voice to get info for. If None, returns all voices.

    Returns:
        Dictionary with voice information.
    """
    if voice:
        if voice in VOICE_DESCRIPTIONS:
            return {voice: VOICE_DESCRIPTIONS[voice]}
        return {}

    return VOICE_DESCRIPTIONS.copy()


def combine_narrations_with_pauses(
    narrations: list[str],
    pause_marker: str = "...",
    pause_between_slides: int = 2
) -> str:
    """Combine multiple narration scripts into one with pauses.

    Args:
        narrations: List of narration scripts for each slide.
        pause_marker: Text marker for pauses (e.g., "..." or "[pause]").
        pause_between_slides: Number of pause markers between slides.

    Returns:
        Combined narration script with pauses.
    """
    pause = f" {pause_marker} " * pause_between_slides
    return pause.join(narrations)


def generate_combined_voiceover(
    narrations: list[str],
    output_dir: str = "./audio",
    output_filename: str = "narration_full.mp3",
    voice: str = "George",
    pause_marker: str = "...",
    pause_count: int = 2
) -> str:
    """Generate a single voiceover for all slides with natural pauses.

    This creates a cohesive narration with consistent voice, tone, and pacing
    across all slides, with pauses between sections.

    Args:
        narrations: List of narration scripts for each slide.
        output_dir: Directory to save audio file.
        output_filename: Name for the output file.
        voice: Voice name (George, Aria, Hope, etc.) or voice ID.
        pause_marker: Text marker for pauses.
        pause_count: Number of pause markers between slides.

    Returns:
        Path to the generated audio file.
    """
    _init_fal()

    # Resolve voice name/ID
    voice_param = _resolve_voice(voice)

    # Combine all narrations with pauses
    combined_script = combine_narrations_with_pauses(
        narrations, pause_marker, pause_count
    )

    print(f"Combined script length: {len(combined_script)} characters")

    def _generate():
        return fal_client.subscribe(
            "fal-ai/elevenlabs/tts/eleven-v3",
            arguments={
                "text": combined_script,
                "voice": voice_param,
                "speed": 1.0,
                "output_format": "mp3_44100_128",
            },
        )

    result = api_call_with_retry(_generate)

    audio_url = result["audio"]["url"]

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    response = requests.get(audio_url)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


def get_audio_duration(audio_path: str) -> float:
    """Get duration of an audio file using ffprobe.

    Args:
        audio_path: Path to audio file.

    Returns:
        Duration in seconds.

    Raises:
        RuntimeError: If ffprobe fails.
    """
    ffprobe = get_ffprobe_path()

    result = subprocess.run(
        [ffprobe, "-v", "quiet", "-print_format", "json", "-show_format", audio_path],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {audio_path}: {result.stderr}")

    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def generate_narrations_with_timing(
    narrations: list[str],
    output_dir: str = "./audio",
    voice: str = "George"
) -> tuple[list[str], list[float]]:
    """Generate individual narration clips and return their durations.

    This allows for per-slide timing based on actual narration length.
    Each narration is generated as a separate audio file.

    Args:
        narrations: List of narration scripts for each slide.
        output_dir: Directory to save audio files.
        voice: Voice name (George, Aria, Hope, etc.) or voice ID.

    Returns:
        Tuple of (list of audio file paths, list of durations in seconds).
    """
    paths = []
    durations = []
    total = len(narrations)

    print(f"Generating {total} individual narration clips...")

    for i, text in enumerate(narrations, 1):
        print(f"  Narration {i}/{total}...")
        path = generate_voiceover(text, i, output_dir, voice)
        duration = get_audio_duration(path)

        paths.append(path)
        durations.append(duration)
        print(f"    Duration: {duration:.1f}s")

    total_duration = sum(durations)
    print(f"  Total narration time: {total_duration:.1f}s")

    return paths, durations


def generate_silence(duration: float, output_path: str, sample_rate: int = 44100) -> str:
    """Generate a silent audio file of specified duration.

    Args:
        duration: Duration in seconds.
        output_path: Path for output file.
        sample_rate: Audio sample rate (default: 44100 Hz).

    Returns:
        Path to the generated silence file.

    Raises:
        RuntimeError: If FFmpeg fails.
    """
    ffmpeg = get_ffmpeg_path()

    result = subprocess.run(
        [
            ffmpeg, "-y",
            "-f", "lavfi",
            "-i", f"anullsrc=r={sample_rate}:cl=stereo",
            "-t", str(duration),
            "-c:a", "libmp3lame",
            "-q:a", "4",
            output_path,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed generating silence: {result.stderr}")

    return output_path


def concatenate_with_gaps(
    audio_files: list[str],
    gap_durations: list[float],
    output_path: str,
    temp_dir: Optional[str] = None
) -> str:
    """Concatenate audio files with silence gaps between them.

    Creates a single audio track: audio1 -> silence1 -> audio2 -> silence2 -> ...
    Note: The last audio file has no gap after it.

    Args:
        audio_files: List of paths to audio files.
        gap_durations: Silence duration after each audio (len = len(audio_files) - 1).
        output_path: Path for final output file.
        temp_dir: Directory for temporary files. Defaults to output directory.

    Returns:
        Path to the concatenated audio file.

    Raises:
        ValueError: If gap count doesn't match audio count - 1.
        RuntimeError: If FFmpeg fails.
    """
    if len(gap_durations) != len(audio_files) - 1:
        raise ValueError(
            f"Gap count ({len(gap_durations)}) must be "
            f"audio count - 1 ({len(audio_files) - 1})"
        )

    ffmpeg = get_ffmpeg_path()

    # Setup temp directory
    if temp_dir is None:
        temp_dir = str(Path(output_path).parent)
    temp_path = Path(temp_dir)
    temp_path.mkdir(parents=True, exist_ok=True)

    # Ensure output directory exists
    output_dir = Path(output_path).parent
    if output_dir and str(output_dir) != ".":
        output_dir.mkdir(parents=True, exist_ok=True)

    segments = []
    silence_files = []
    concat_file = str(temp_path / "audio_concat.txt")

    try:
        # Build segment list: audio1, silence1, audio2, silence2, ..., audioN
        for i, audio in enumerate(audio_files):
            segments.append(audio)

            # Add silence gap (except after last audio)
            if i < len(gap_durations):
                silence_path = str(temp_path / f"silence_{i + 1:02d}.mp3")
                print(f"  Creating silence gap {i + 1} ({gap_durations[i]:.1f}s)...")
                generate_silence(gap_durations[i], silence_path)
                segments.append(silence_path)
                silence_files.append(silence_path)

        # Create concat file
        with open(concat_file, "w", encoding="utf-8") as f:
            for seg in segments:
                seg_path = Path(seg).resolve()
                seg_str = str(seg_path).replace("\\", "/")
                f.write(f"file '{seg_str}'\n")

        # Concatenate all audio segments
        print("  Concatenating audio segments...")
        result = subprocess.run(
            [
                ffmpeg, "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_file,
                "-c:a", "libmp3lame",
                "-q:a", "2",
                output_path,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg failed concatenating audio: {result.stderr}")

        # Get final duration
        final_duration = get_audio_duration(output_path)
        print(f"  Combined audio duration: {final_duration:.1f}s")
        print(f"  Saved: {output_path}")

        return output_path

    finally:
        # Clean up temporary silence files
        for sf in silence_files:
            if os.path.exists(sf):
                os.remove(sf)
        # Clean up concat file
        if os.path.exists(concat_file):
            os.remove(concat_file)