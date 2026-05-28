---
name: youtube-transcript
description: Use this skill when you want to extract or download transcripts, subtitles, or captions from YouTube videos by providing a YouTube URL or asking for a transcript.
---

# YouTube Transcript Skill

This skill helps you download transcripts (subtitles/captions) from YouTube videos using yt-dlp or the youtube-transcript-api.

## When to Use This Skill

Activate this skill when you:
- Provide a YouTube URL and want the transcript
- Ask to "download transcript from YouTube"
- Want to "get captions" or "get subtitles" from a video
- Ask to "transcribe a YouTube video"
- Need text content from a YouTube video

## How It Works

### Default Workflow:
1. **Check if yt-dlp is installed** - install if needed.
2. **List available subtitles** - see what's available for the provided URL.
3. **Try manual subtitles first** (`--write-sub`) - highest quality, human-created.
4. **Fallback to auto-generated** (`--write-auto-sub`) - usually available.
5. **Use youtube-transcript-api** if no subtitles are available.
6. **Convert to plain text** - deduplicate and clean up VTT format if necessary.
7. **Save the transcript** as a markdown or text file with a filename based on the video title.
8. **Confirm the download** and show the user where the file is saved.

## Installation Check

**IMPORTANT**: Always check if yt-dlp is installed first:

```bash
which yt-dlp || command -v yt-dlp
```

### If Not Installed

Attempt automatic installation based on the system:

**macOS (Homebrew)**:
```bash
brew install yt-dlp
```

**Linux (apt/Debian/Ubuntu)**:
```bash
sudo apt update && sudo apt install -y yt-dlp
```

**Alternative (pip - works on all systems)**:
```bash
pip3 install yt-dlp
# or
python3 -m pip install yt-dlp
```

**If installation fails**: Inform the user they need to install yt-dlp manually and provide them with installation instructions from https://github.com/yt-dlp/yt-dlp#installation.

## Check Available Subtitles

**ALWAYS do this first** before attempting to download:

```bash
yt-dlp --list-subs "YOUTUBE_URL"
```

This shows what subtitle types are available without downloading anything. Look for:
- Manual subtitles (better quality)
- Auto-generated subtitles (usually available)
- Available languages

## Output Format

- If the transcript is without timestamps, clean it up so that it is arranged by complete paragraphs.
- If you were asked to save the transcript to a specific file, save it to the requested file.
- If no output file was specified, use the YouTube video ID with a `-transcript.txt` suffix.

## Notes

- Fetches auto-generated or manually added captions (whichever is available).
- Requires the video to have captions enabled.
- Falls back to auto-generated captions if manual ones aren't available.