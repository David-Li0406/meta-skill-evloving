#!/bin/bash
# Download YouTube video in medium quality (720p or lower)
# Usage: ./download-youtube.sh <youtube-url>

if [ -z "$1" ]; then
    echo "Error: YouTube URL required"
    echo "Usage: $0 <youtube-url>"
    exit 1
fi

YOUTUBE_URL="$1"

# Check if yt-dlp is installed
if ! command -v yt-dlp &> /dev/null; then
    echo "Error: yt-dlp is not installed"
    echo "Install with: pip install yt-dlp"
    echo "Or: brew install yt-dlp (macOS)"
    echo "Or: sudo apt install yt-dlp (Ubuntu/Debian)"
    exit 1
fi

# Download video in medium quality (720p max), output as video.mp4
echo "Downloading YouTube video..."
yt-dlp \
    -f "bestvideo[height<=720]+bestaudio/best[height<=720]" \
    --merge-output-format mp4 \
    -o "video.mp4" \
    "$YOUTUBE_URL"

if [ $? -eq 0 ]; then
    echo "✓ Video downloaded successfully as video.mp4"
else
    echo "Error: Failed to download video"
    exit 1
fi
