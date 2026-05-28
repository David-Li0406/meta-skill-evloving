---
name: youtube-transcript-extraction
description: Use this skill to extract transcripts, subtitles, or captions from YouTube videos when a user provides a YouTube URL or requests a transcript.
---

# YouTube Transcript Extraction

This skill allows you to download transcripts (subtitles/captions) from YouTube videos using various methods, including direct API calls and fallback options.

## When to Use This Skill

Activate this skill when the user:
- Provides a YouTube URL and wants the transcript
- Asks to "download transcript from YouTube"
- Wants to "get captions" or "get subtitles" from a video
- Asks to "transcribe a YouTube video"
- Needs text content from a YouTube video

## How It Works

### Default Workflow:
1. **Check if yt-dlp is installed** - install if needed.
2. **List available subtitles** - see what's actually available.
3. **Try manual subtitles first** (`--write-sub`) - highest quality.
4. **Fallback to auto-generated** (`--write-auto-sub`) - usually available.
5. **Last resort: Whisper transcription** - if no subtitles exist (requires user confirmation).
6. **Confirm the download** and show the user where the file is saved.
7. **Optionally clean up** the VTT format if the user wants plain text.

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

## Download Strategy

### Option 1: Manual Subtitles (Preferred)

Try this first - highest quality, human-created:

```bash
yt-dlp --write-sub --skip-download --output "OUTPUT_NAME" "YOUTUBE_URL"
```

### Option 2: Auto-Generated Subtitles (Fallback)

If manual subtitles aren't available:

```bash
yt-dlp --write-auto-sub --skip-download --output "OUTPUT_NAME" "YOUTUBE_URL"
```

Both commands create a `.vtt` file (WebVTT subtitle format).

### Option 3: Whisper Transcription (Last Resort)

**ONLY use this if both manual and auto-generated subtitles are unavailable.**

1. **Show File Size and Ask for Confirmation**:
   ```bash
   yt-dlp --print "%(filesize_approx)s" -f "bestaudio" "YOUTUBE_URL"
   ```

2. **Check for Whisper Installation**:
   ```bash
   command -v whisper
   ```

3. **Download Audio Only**:
   ```bash
   yt-dlp -x --audio-format mp3 --output "audio_%(id)s.%(ext)s" "YOUTUBE_URL"
   ```

4. **Transcribe with Whisper**:
   ```bash
   whisper audio_VIDEO_ID.mp3 --model base --output_format vtt
   ```

5. **Cleanup**:
   After transcription completes, ask the user if they want to delete the audio file.

## Post-Processing

### Convert to Plain Text (Recommended)

YouTube's auto-generated VTT files contain **duplicate lines**. Always deduplicate when converting to plain text while preserving the original speaking order.

```bash
python3 -c "
import sys, re
seen = set()
with open('transcript.en.vtt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line:
            clean = re.sub('<[^>]*>', '', line)
            clean = clean.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
            if clean and clean not in seen:
                print(clean)
                seen.add(clean)
" > transcript.txt
```

## Output Formats

- **VTT format** (`.vtt`): Includes timestamps and formatting, good for video players.
- **Plain text** (`.txt`): Just the text content, good for reading or analysis.

## Error Handling

### Common Issues and Solutions:

1. **yt-dlp not installed**: Attempt automatic installation based on system.
2. **No subtitles available**: List available subtitles first to confirm.
3. **Invalid or private video**: Check if URL is correct format.
4. **Download interrupted or failed**: Check internet connection and disk space.

### Best Practices:

- ✅ Always check what's available before attempting download (`--list-subs`).
- ✅ Try manual subtitles first (`--write-sub`), then fall back to auto-generated.
- ✅ Convert VTT to plain text format for easy reading.
- ✅ Deduplicate text content to remove caption overlaps.
- ✅ Provide clear feedback about what's happening at each stage.