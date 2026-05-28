---
name: pm7y-youtube-transcript
description: Download YouTube video transcripts and create structured summaries when user provides a YouTube URL or asks to download/get/fetch a transcript from YouTube. Also use when user wants to transcribe or get captions/subtitles from a YouTube video.
allowed-tools: Bash,Read,Write
---

# YouTube Transcript Summary Generator

This skill downloads transcripts from YouTube videos and creates a structured `TRANSCRIPT.md` summary with key points (including time codes) and a detailed description. It does NOT include the full transcript text.

**Cross-platform:** Works on Windows, macOS, and Linux using Python.

## When to Use This Skill

Activate this skill when the user:
- Provides a YouTube URL and wants the transcript
- Asks to "download transcript from YouTube"
- Wants to "get captions" or "get subtitles" from a video
- Asks to "transcribe a YouTube video"
- Needs text content from a YouTube video

## Output Format

The skill produces a `TRANSCRIPT.md` file containing:
1. **Video metadata** - title, URL
2. **Summary** - brief overview of the video content
3. **Key Points** - main takeaways with time codes (e.g., `[02:34]`)
4. **Detailed Description** - expanded explanation of the content

**Note:** The full transcript text is NOT included in the output.

## How It Works

### Priority Order:
1. **Check if youtube-transcript-api is installed** - install if needed
2. **Extract video ID** from the YouTube URL
3. **Fetch transcript with timestamps** using the API
4. **Get video title** from YouTube
5. **Save timestamped transcript** to temporary file
6. **Analyze and summarize** - identify key points and generate summary
7. **Write TRANSCRIPT.md** - create structured markdown file
8. **Clean up** temporary files

## Installation Check

**IMPORTANT**: Always check if youtube-transcript-api is installed first:

```bash
python -c "import youtube_transcript_api" 2>/dev/null || python3 -c "import youtube_transcript_api" 2>/dev/null
```

### If Not Installed

Install the package (works on all platforms):

```bash
pip install youtube-transcript-api
```

Or with python3:
```bash
pip3 install youtube-transcript-api
```

## Extract Video ID

YouTube URLs come in various formats. Extract the video ID:

| URL Format | Video ID |
|------------|----------|
| `https://www.youtube.com/watch?v=ABC123` | `ABC123` |
| `https://youtu.be/ABC123` | `ABC123` |
| `https://www.youtube.com/embed/ABC123` | `ABC123` |

## Fetch Transcript with Timestamps

Use this Python script to fetch the transcript. It works cross-platform (Windows/macOS/Linux):

```python
import sys
import json
import re
import urllib.request
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/|/embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'  # Just the ID
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_title(video_id):
    """Fetch video title from YouTube page."""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            match = re.search(r'<title>([^<]+)</title>', html)
            if match:
                title = match.group(1).replace(' - YouTube', '').strip()
                return title
    except:
        pass
    return f"YouTube Video {video_id}"

def format_timestamp(seconds):
    """Convert seconds to MM:SS or HH:MM:SS format."""
    seconds = int(seconds)
    if seconds >= 3600:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

def main(url_or_id):
    video_id = get_video_id(url_or_id)
    if not video_id:
        print(f"Error: Could not extract video ID from: {url_or_id}", file=sys.stderr)
        sys.exit(1)

    # Get video title
    title = get_video_title(video_id)
    print(f"TITLE: {title}")
    print(f"URL: https://www.youtube.com/watch?v={video_id}")
    print("---TRANSCRIPT---")

    # Fetch transcript (API v1.2+ requires instance)
    api = YouTubeTranscriptApi()
    try:
        transcript = api.fetch(video_id)
    except Exception as e:
        # Try with auto-generated
        try:
            transcript_list = api.list(video_id)
            transcript = transcript_list.find_generated_transcript(['en']).fetch()
        except Exception as e2:
            print(f"Error: Could not fetch transcript: {e2}", file=sys.stderr)
            sys.exit(1)

    # Output timestamped transcript (entries are objects with .start/.text attributes)
    for entry in transcript:
        timestamp = format_timestamp(entry.start)
        text = entry.text.replace('\n', ' ').strip()
        print(f"[{timestamp}] {text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <youtube_url_or_id>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
```

## Complete Workflow

### Step 1: Check/Install youtube-transcript-api

**On macOS/Linux:**
```bash
python3 -c "import youtube_transcript_api" 2>/dev/null || pip3 install youtube-transcript-api
```

**On Windows (PowerShell):**
```powershell
python -c "import youtube_transcript_api" 2>$null; if ($LASTEXITCODE -ne 0) { pip install youtube-transcript-api }
```

### Step 2: Fetch Transcript

Save the Python script above to a temporary file and run it:

**Cross-platform approach** - Write and execute inline Python:

```bash
python3 << 'PYEOF' > transcript_with_timestamps.txt
import sys
import re
import urllib.request
from youtube_transcript_api import YouTubeTranscriptApi

VIDEO_URL = "REPLACE_WITH_URL"

def get_video_id(url):
    patterns = [r'(?:v=|/v/|youtu\.be/|/embed/)([a-zA-Z0-9_-]{11})', r'^([a-zA-Z0-9_-]{11})$']
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_title(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            match = re.search(r'<title>([^<]+)</title>', html)
            if match:
                return match.group(1).replace(' - YouTube', '').strip()
    except:
        pass
    return f"YouTube Video {video_id}"

def format_timestamp(seconds):
    seconds = int(seconds)
    if seconds >= 3600:
        return f"{seconds // 3600}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"
    return f"{seconds // 60:02d}:{seconds % 60:02d}"

video_id = get_video_id(VIDEO_URL)
title = get_video_title(video_id)
print(f"TITLE: {title}")
print(f"URL: https://www.youtube.com/watch?v={video_id}")
print("---TRANSCRIPT---")

# API v1.2+ requires instance
api = YouTubeTranscriptApi()
try:
    transcript = api.fetch(video_id)
except:
    transcript_list = api.list(video_id)
    transcript = transcript_list.find_generated_transcript(['en']).fetch()

# Entries are objects with .start/.text attributes
for entry in transcript:
    ts = format_timestamp(entry.start)
    text = entry.text.replace('\n', ' ').strip()
    print(f"[{ts}] {text}")
PYEOF
```

**On Windows (PowerShell)** - Use a temporary .py file:

```powershell
$script = @'
import sys, re, urllib.request
from youtube_transcript_api import YouTubeTranscriptApi

VIDEO_URL = "REPLACE_WITH_URL"

# ... (same Python code as above)
'@
$script | Out-File -Encoding utf8 temp_transcript.py
python temp_transcript.py > transcript_with_timestamps.txt
Remove-Item temp_transcript.py
```

### Step 3: Analyze and Create TRANSCRIPT.md

After running the above, you MUST:

1. **Read** the `transcript_with_timestamps.txt` file
2. **Extract** the TITLE and URL from the first lines
3. **Analyze** the transcript content to identify:
   - Main topics covered
   - Key points with their time codes
   - Overall theme and purpose
4. **Write** a `TRANSCRIPT.md` file with this structure:

```markdown
# [Video Title]

**Source:** [YouTube URL]

## Summary

[2-3 paragraph overview of what the video covers]

## Key Points

- **[Key Point 1]** `[MM:SS]` - Brief description of this point
- **[Key Point 2]** `[MM:SS]` - Brief description of this point
- **[Key Point 3]** `[MM:SS]` - Brief description of this point
[... more key points as appropriate]

## Detailed Description

[Expanded explanation of the video content, organized by topic or chronologically. Reference time codes where helpful for specific topics, e.g., "The speaker discusses X starting at `[05:23]`..."]
```

### Step 4: Clean Up

Delete temporary files:

**macOS/Linux:**
```bash
rm transcript_with_timestamps.txt
```

**Windows (PowerShell):**
```powershell
Remove-Item transcript_with_timestamps.txt
```

## Important Guidelines for TRANSCRIPT.md

- Identify 5-15 key points depending on video length
- Each key point MUST include a time code in `[MM:SS]` format
- Time codes should link to significant moments (topic changes, important statements, demonstrations)
- The detailed description should synthesize the content, not just repeat the key points
- Do NOT include the raw transcript text

## Error Handling

### Common Issues and Solutions:

**1. youtube-transcript-api not installed**
- Run: `pip install youtube-transcript-api` or `pip3 install youtube-transcript-api`
- If pip not found, ensure Python is installed and in PATH

**2. No transcript available**
- Some videos have captions disabled
- Try listing available transcripts: `YouTubeTranscriptApi.list_transcripts(video_id)`
- May need to try different language codes

**3. Video is private or age-restricted**
- The API cannot access private videos
- Age-restricted videos may require authentication

**4. Invalid URL format**
- Ensure URL is a valid YouTube URL
- Supported formats: `youtube.com/watch?v=ID`, `youtu.be/ID`, `youtube.com/embed/ID`

**5. Python not found**
- On Windows, ensure Python is installed and added to PATH
- Try both `python` and `python3` commands
