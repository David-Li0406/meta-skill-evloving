#!/usr/bin/env bash

# transcribe-audio.sh - Transcribe audio using ElevenLabs API
# Usage: transcribe-audio.sh <language-code>

set -euo pipefail

LANGUAGE_CODE="$1"

if [ -z "${ELEVENLABS_API_KEY:-}" ]; then
    echo "Error: ELEVENLABS_API_KEY environment variable not set" >&2
    exit 1
fi

if [ ! -f "audio.mp3" ]; then
    echo "Error: audio.mp3 not found" >&2
    exit 1
fi

TEMP_JSON=$(mktemp)
trap "rm -f $TEMP_JSON" EXIT

# Call ElevenLabs API
curl -X POST "https://api.elevenlabs.io/v1/speech-to-text" \
    -H "xi-api-key: $ELEVENLABS_API_KEY" \
    -F "model_id=scribe_v1" \
    -F "file=@audio.mp3" \
    -F "language_code=$LANGUAGE_CODE" \
    -o "$TEMP_JSON" \
    -s

# Check for errors
if ! jq empty "$TEMP_JSON" 2>/dev/null; then
    echo "Error: Invalid API response" >&2
    cat "$TEMP_JSON" >&2
    exit 1
fi

if jq -e '.detail' "$TEMP_JSON" >/dev/null 2>&1; then
    echo "API Error:" >&2
    jq -r '.detail' "$TEMP_JSON" >&2
    exit 1
fi

# Extract and save transcript
jq -r '.text' "$TEMP_JSON" > generated-transcript.txt

echo "Transcript saved: generated-transcript.txt"
