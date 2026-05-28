#!/usr/bin/env python3
"""
Deepgram Audio/Video Transcription Script

This script handles transcription of audio and video files using the Deepgram API.
For large video files, it first extracts audio to reduce upload size and time.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
import requests


def extract_audio(video_path, output_path, bitrate="128k"):
    """
    Extract audio from video file using ffmpeg.

    Args:
        video_path: Path to input video file
        output_path: Path for output audio file
        bitrate: Audio bitrate (default: 128k)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cmd = [
            "ffmpeg", "-i", video_path,
            "-vn",  # No video
            "-acodec", "aac",
            "-b:a", bitrate,
            output_path,
            "-y"  # Overwrite output
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error extracting audio: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg.", file=sys.stderr)
        return False


def transcribe_with_deepgram(file_path, api_key, model="nova-2", smart_format=True):
    """
    Transcribe audio/video file using Deepgram API.

    Args:
        file_path: Path to audio/video file
        api_key: Deepgram API key
        model: Deepgram model to use (default: nova-2)
        smart_format: Enable smart formatting (default: True)

    Returns:
        dict: Transcription result from Deepgram API, or None if failed
    """
    url = f"https://api.deepgram.com/v1/listen?model={model}&smart_format={str(smart_format).lower()}"

    # Determine content type based on file extension
    ext = Path(file_path).suffix.lower()
    content_types = {
        '.mp4': 'video/mp4',
        '.mov': 'video/quicktime',
        '.m4a': 'audio/mp4',
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.aac': 'audio/aac',
    }
    content_type = content_types.get(ext, 'application/octet-stream')

    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": content_type
    }

    try:
        with open(file_path, 'rb') as f:
            response = requests.post(url, headers=headers, data=f, timeout=300)
            response.raise_for_status()
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Deepgram API: {e}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return None


def save_transcription(result, output_dir, base_name):
    """
    Save transcription results to JSON and text files.

    Args:
        result: Deepgram API response
        output_dir: Directory to save files
        base_name: Base filename (without extension)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save full JSON response
    json_path = output_dir / f"{base_name}_transcription.json"
    with open(json_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Saved full transcription JSON: {json_path}")

    # Extract and save plain text transcript
    try:
        transcript = result['results']['channels'][0]['alternatives'][0]['transcript']
        txt_path = output_dir / f"{base_name}_transcript.txt"
        with open(txt_path, 'w') as f:
            f.write(transcript)
        print(f"Saved plain text transcript: {txt_path}")
    except (KeyError, IndexError) as e:
        print(f"Warning: Could not extract transcript text: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio/video files using Deepgram API"
    )
    parser.add_argument("input_file", help="Path to audio or video file")
    parser.add_argument("--api-key", required=True, help="Deepgram API key")
    parser.add_argument("--output-dir", default=".", help="Output directory for transcripts")
    parser.add_argument("--model", default="nova-2", help="Deepgram model (default: nova-2)")
    parser.add_argument("--no-smart-format", action="store_true", help="Disable smart formatting")
    parser.add_argument("--extract-audio", action="store_true",
                       help="Extract audio from video first (recommended for large files)")
    parser.add_argument("--audio-bitrate", default="128k", help="Audio bitrate when extracting (default: 128k)")

    args = parser.parse_args()

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        return 1

    # Determine file to transcribe
    file_to_transcribe = input_path
    temp_audio_file = None

    # Extract audio if requested or if file is large video
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv'}
    file_size_mb = input_path.stat().st_size / (1024 * 1024)

    if args.extract_audio or (input_path.suffix.lower() in video_extensions and file_size_mb > 50):
        print(f"Extracting audio from {input_path.name}...")
        temp_audio_file = Path(args.output_dir) / f"{input_path.stem}_audio.m4a"

        if not extract_audio(str(input_path), str(temp_audio_file), args.audio_bitrate):
            return 1

        file_to_transcribe = temp_audio_file
        print(f"Audio extracted: {temp_audio_file} ({temp_audio_file.stat().st_size / (1024*1024):.1f} MB)")

    # Transcribe
    print(f"Transcribing {file_to_transcribe.name} using Deepgram...")
    result = transcribe_with_deepgram(
        str(file_to_transcribe),
        args.api_key,
        model=args.model,
        smart_format=not args.no_smart_format
    )

    if result is None:
        return 1

    # Save results
    save_transcription(result, args.output_dir, input_path.stem)

    # Clean up temporary audio file if created
    if temp_audio_file and temp_audio_file.exists():
        temp_audio_file.unlink()
        print(f"Cleaned up temporary file: {temp_audio_file}")

    print("\n✅ Transcription completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
