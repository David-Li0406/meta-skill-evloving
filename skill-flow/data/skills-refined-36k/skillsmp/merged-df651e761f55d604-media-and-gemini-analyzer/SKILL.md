---
name: media-and-gemini-analyzer
description: Use this skill when you need to analyze media files (images, audio, video) using the Gemini API and gather information through web searches or API data collection.
---

# Media and Gemini Analyzer

This skill utilizes the Gemini API to analyze images, audio, and video files, as well as to gather information through web searches and API data collection.

## Requirements

```bash
# Install dependencies
pip install google-genai

# Set environment variable
export GEMINI_API_KEY="your_api_key"
```

## Usage

### Analyze Local Files
```bash
python analyze.py /path/to/audio.mp3
python analyze.py /path/to/video.mp4
```

### Analyze from URL
```bash
python analyze.py "https://example.com/audio.mp3"
```

### Analyze with Custom Prompt
```bash
python analyze.py /path/to/file.mp3 --prompt "Analyze the genre and mood of this song"
```

### Detailed Mode
```bash
python analyze.py /path/to/file.mp4 --verbose
```

## Supported Formats

### Images
- JPG, JPEG, PNG, GIF, WebP, BMP, TIFF

### Audio
- MP3, WAV, AAC, FLAC, OGG, M4A

### Video
- MP4, AVI, MOV, MKV, WebM

## Example Output

```
=== Media Analysis Result ===
File: example.mp3
Type: audio/mpeg

[Analysis Content]
This song is a fast-paced electronic music piece...
```

## Environment Variables

| Variable Name     | Description            | Required |
|-------------------|------------------------|----------|
| GEMINI_API_KEY    | Gemini API Key         | Yes      |

## Troubleshooting

### API Key Error
```
export GEMINI_API_KEY="your_key_here"
```

### File Size Limitations
Large files will be automatically processed in chunks.