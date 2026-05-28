#!/usr/bin/env python3
"""
Fetch YouTube transcript directly using youtube-transcript-api.

This script fetches transcripts without using the MCP tool, avoiding context pollution.
It replicates the functionality of the MCP youtube-transcript server.
"""

import sys
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)


def extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from URL."""
    import re
    from urllib.parse import urlparse, parse_qs

    # Handle short URL format
    if 'youtu.be/' in url:
        match = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', url)
        if match:
            return match.group(1)

    # Handle standard watch URL
    parsed = urlparse(url)
    if parsed.hostname in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
        if parsed.path == '/watch':
            query_params = parse_qs(parsed.query)
            if 'v' in query_params:
                return query_params['v'][0]
        elif parsed.path.startswith('/embed/'):
            return parsed.path.split('/')[2]
        elif parsed.path.startswith('/v/'):
            return parsed.path.split('/')[2]

    return None


def fetch_transcript(video_id: str, lang: str = 'en') -> dict:
    """
    Fetch transcript for a YouTube video.

    Args:
        video_id: YouTube video ID
        lang: Language code (default: 'en')

    Returns:
        Dictionary with:
        - success: bool
        - transcript: list of segments (if successful)
        - error: str (if failed)
        - metadata: dict with title, etc. (if available)
    """
    try:
        # Create API instance
        api = YouTubeTranscriptApi()

        # Fetch transcript with language preference
        transcript_list = api.list(video_id)

        # Try to get transcript in requested language
        try:
            transcript = transcript_list.find_transcript([lang])
        except NoTranscriptFound:
            # Fallback to English
            try:
                transcript = transcript_list.find_transcript(['en'])
                lang = 'en'
            except NoTranscriptFound:
                # Use first available transcript
                first_transcript = list(transcript_list)[0]
                transcript = transcript
                lang = first_transcript.language_code

        # Fetch the actual transcript data
        transcript_obj = transcript.fetch()

        # Get video metadata (if available)
        metadata = {
            'title': '',  # Not directly available from this API
            'language': transcript.language_code,
            'is_generated': transcript.is_generated
        }

        # Convert transcript object to list of dicts
        transcript_data = []
        for segment in transcript_obj:
            transcript_data.append({
                'text': segment.text,
                'start': segment.start,
                'duration': segment.duration
            })

        return {
            'success': True,
            'transcript': transcript_data,
            'metadata': metadata,
            'requested_lang': lang
        }

    except TranscriptsDisabled:
        return {
            'success': False,
            'error': 'Transcripts are disabled for this video'
        }
    except NoTranscriptFound:
        return {
            'success': False,
            'error': 'No transcript found for this video'
        }
    except VideoUnavailable:
        return {
            'success': False,
            'error': 'Video is unavailable'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }


def main():
    """
    Main entry point.

    Input (stdin JSON):
    {
        "url": "https://youtube.com/watch?v=...",
        "lang": "en"  // Optional, defaults to "en"
    }

    Output (stdout JSON):
    {
        "success": true,
        "video_id": "abc123",
        "transcript": [{"text": "...", "start": 0.0, "duration": 1.5}, ...],
        "metadata": {"title": "...", "language": "en", ...}
    }
    """
    try:
        # Read input
        input_data = json.load(sys.stdin)
        url = input_data.get("url")
        lang = input_data.get("lang", "en")

        if not url:
            print(json.dumps({
                "success": False,
                "error": "No URL provided"
            }))
            sys.exit(1)

        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            print(json.dumps({
                "success": False,
                "error": "Invalid YouTube URL"
            }))
            sys.exit(1)

        # Fetch transcript
        result = fetch_transcript(video_id, lang)

        # Add video ID to result
        result['video_id'] = video_id

        print(json.dumps(result, indent=2))

        if not result['success']:
            sys.exit(1)

    except json.JSONDecodeError:
        print(json.dumps({
            "success": False,
            "error": "Invalid JSON input"
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
