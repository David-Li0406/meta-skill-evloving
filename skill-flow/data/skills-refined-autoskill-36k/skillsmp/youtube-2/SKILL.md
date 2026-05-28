---
name: youtube
description: Handle YouTube links and transcripts. Use when the user (1) pastes a YouTube URL that needs cleaning to short form, (2) requests transcript fetching from YouTube videos, or (3) works with YouTube video content. Automatically cleans URLs to https://youtu.be/VIDEO_ID format and saves transcripts directly to Database/Bookmarks to avoid polluting chat context.
---

# YouTube

## Overview

This skill handles YouTube links and transcript operations. It automatically cleans YouTube URLs to canonical short form and fetches transcripts using the MCP YouTube transcript tool, saving them directly to the Bookmarks database to avoid filling up chat context.

## Core Capabilities

### 1. URL Cleaning

When YouTube URLs are encountered (pasted, mentioned, or used), automatically clean them:

**Always convert to short form:** `https://youtu.be/<id>`

**Remove all:**
- Query parameters (e.g., `?v=`, `?si=`, `&feature=`, etc.)
- Tracking identifiers
- Playlist parameters
- Timestamp parameters

**Supported input formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID` (any query params)
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID` (any query params)
- `https://m.youtube.com/watch?v=VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

**Use the utility script:**

```python
from scripts.youtube_utils import clean_youtube_url, extract_video_id

# Clean any YouTube URL
clean_url = clean_youtube_url(dirty_url)
# Result: "https://youtu.be/eIoohUmYpGI"

# Or just extract the ID
video_id = extract_video_id(dirty_url)
# Result: "eIoohUmYpGI"
```

### 2. Transcript Fetching and Saving to Bookmarks

**Key principle:** Save transcripts directly to `Database/Bookmarks` to avoid polluting chat context with full transcript content. This allows handling multiple video links without context overflow.

**Output location:** `Database/Bookmarks/youtube-{video_id}.md`

**Caching:** The Database/Bookmarks directory acts as a cache. If a video already has a bookmark file with a valid transcript (not empty/failed), it won't be re-fetched unless forced.

**Workflow:**

1. **Clean the URL** using `clean_youtube_url(url)` to get canonical short form
2. **Check if bookmark exists** - if valid transcript exists, skip fetching
3. **Fetch transcript** using `mcp__youtube-transcript__get_transcript` MCP tool (only if not cached)
4. **Save directly to Bookmarks** using the `save_transcript.py` script
5. **Return only success message** with `cached` flag (not the full transcript)

**Simplified workflow for Claude:**

When a user provides a YouTube URL, use the `process_youtube_url.py` script which handles everything:

```bash
echo '{"url": "URL", "lang": "en", "force": false}' | \
  python3 .claude/skills/youtube/scripts/process_youtube_url.py
```

This single command:
1. Checks if transcript is already cached in Bookmarks
2. If cached, returns immediately with `cached: true`
3. If not cached, fetches transcript directly using youtube-transcript-api (Python library)
4. Saves to Database/Bookmarks with proper formatting
5. Returns success status without showing full transcript content

**Output:**
```json
{
  "success": true,
  "video_id": "abc123",
  "filepath": "Database/Bookmarks/youtube-abc123.md",
  "url": "https://youtu.be/abc123",
  "title": "Video Title",
  "cached": false
}
```

**Benefits:**
- No MCP tool needed - fetches transcripts directly
- NO context pollution - transcript never appears in chat
- Automatic caching - same video won't be fetched twice
- Single command - no multi-step workflow needed

**Important:**
- **Check cache first** to avoid redundant API calls
- DO NOT return the full transcript text in chat
- Only inform the user that the transcript was saved/cached
- Use the `cached` flag in output to inform user if existing bookmark was used
- This prevents context pollution when handling multiple videos
- Users can read the transcript from the bookmark file later
- Failed/empty transcripts are NOT cached and will be retried on next request

### 3. Language Support

The MCP transcript tool supports multiple languages via the `lang` parameter:
- Default: `"en"` (English)
- Other examples: `"ko"` (Korean), `"es"` (Spanish), `"fr"` (French), etc.

Always use `"en"` unless the user specifically requests a different language.

## Resources

### scripts/process_youtube_url.py

**Primary entry point** - Use this script for all YouTube transcript operations.

Handles the complete workflow: cache checking → fetching → saving.

**Input (stdin JSON):**
```json
{
  "url": "https://youtube.com/watch?v=...",
  "lang": "en",  // Optional, defaults to "en"
  "force": false  // Optional, force re-fetch even if cached
}
```

**Output (stdout JSON):**
```json
{
  "success": true,
  "video_id": "abc123",
  "filepath": "Database/Bookmarks/youtube-abc123.md",
  "url": "https://youtu.be/abc123",
  "title": "Video Title",
  "cached": false
}
```

### scripts/fetch_transcript.py

Fetches YouTube transcripts using the `youtube-transcript-api` Python library.

Called internally by `process_youtube_url.py`. Uses YouTube's internal API to retrieve transcripts with language fallback support (requested lang → English → first available).

### scripts/save_transcript.py

Saves transcript data to Bookmarks database with proper formatting.

**Purpose:** Write transcript content directly to `Database/Bookmarks/youtube-{video_id}.md` to avoid polluting chat context.

**Input (stdin JSON):**
```json
{
  "url": "https://youtube.com/watch?v=...",
  "title": "Video Title",
  "transcript": [{"text": "...", "start": 0.0, "duration": 1.5}, ...],
  "force": false  // Optional: force re-fetch even if cached
}
```

**Output (stdout JSON):**
```json
{
  "success": true,
  "video_id": "abc123",
  "filepath": "Database/Bookmarks/youtube-abc123.md",
  "url": "https://youtu.be/abc123",
  "title": "Video Title",
  "cached": false  // True if existing valid transcript was found
}
```

**Key features:**
- **Checks cache first** - if bookmark exists with valid transcript, returns immediately
- Only re-fetches if bookmark doesn't exist, has empty/failed transcript, or `force: true`
- Concatenates transcript segments into continuous text
- Creates properly formatted bookmark markdown with frontmatter
- Automatically creates `Database/Bookmarks` directory if needed
- Returns only metadata (not full transcript) to avoid context pollution
- `cached` flag indicates whether existing bookmark was used

### scripts/youtube_utils.py

Python utility module providing URL manipulation functions:

**URL utilities:**
- `extract_video_id(url)`: Extract video ID from any YouTube URL format
- `clean_youtube_url(url)`: Convert any URL to clean `https://youtu.be/<id>` form

The script is self-contained and can be executed directly for testing URL cleaning functionality.

## Best Practices

1. **Always clean URLs** when YouTube links are pasted or referenced to canonical short form
2. **Check cache first** before fetching transcripts to avoid redundant API calls
3. **Save transcripts to Bookmarks** using `save_transcript.py` to avoid context pollution
4. **DO NOT output full transcript** in chat - only inform user of saved/cached location
5. **Use English by default** for transcripts unless user specifies otherwise
6. **Handle multiple videos efficiently** - the Bookmarks approach allows processing many videos without context overflow
7. **Inform user clearly** whether transcript was fetched or loaded from cache
8. **Retry failed transcripts** - empty/failed transcripts are not cached and will be retried
9. **Use `force: true`** only when user explicitly wants to re-fetch existing transcripts
