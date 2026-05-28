#!/usr/bin/env bash

# extract-audio.sh - Extract audio from video file for lecture transcription
# Usage: extract-audio.sh <video-file>

set -euo pipefail

VIDEO_FILE="$1"

if [ ! -f "$VIDEO_FILE" ]; then
    echo "Error: Video file '$VIDEO_FILE' not found" >&2
    exit 1
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "Error: ffmpeg not found" >&2
    exit 1
fi

# Extract audio to audio.mp3
ffmpeg -i "$VIDEO_FILE" -vn -acodec libmp3lame -q:a 2 audio.mp3 -y 2>&1 | grep -v "^frame="

echo "Audio extracted: audio.mp3"
