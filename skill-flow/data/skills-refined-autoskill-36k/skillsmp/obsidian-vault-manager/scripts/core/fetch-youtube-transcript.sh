#!/bin/bash
# Fetch YouTube transcript using youtube_transcript_api
# Usage: ./fetch-youtube-transcript.sh VIDEO_ID

VIDEO_ID="$1"

if [[ -z "$VIDEO_ID" ]]; then
    echo "❌ Error: VIDEO_ID required" >&2
    exit 1
fi

# Fetch transcript using uvx
TRANSCRIPT=$(uvx youtube_transcript_api "$VIDEO_ID" --format text 2>&1)

if [[ $? -ne 0 ]]; then
    echo "❌ Error fetching transcript: $TRANSCRIPT" >&2
    exit 1
fi

# Output transcript to stdout
echo "$TRANSCRIPT"
