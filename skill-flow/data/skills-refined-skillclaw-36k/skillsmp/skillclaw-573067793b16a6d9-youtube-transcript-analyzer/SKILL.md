---
name: youtube-transcript-analyzer
description: Use this skill when analyzing YouTube videos for research or learning to extract insights and understand concepts.
---

# Skill body

## Objective
Download and analyze YouTube video transcripts to extract insights, understand concepts, and relate content to your work. Uses `yt-dlp` for reliable transcript extraction with intelligent chunking for long-form content.

## When to Use
Use when you need to understand how a YouTube video/tutorial relates to your current project, research technical concepts explained in video format, extract key insights from talks or presentations, compare video content with your codebase or approach, or learn from video demonstrations without watching the entire video.

## Prerequisites
Ensure `yt-dlp` is installed:

```bash
# Install via pip
pip install yt-dlp

# Or via homebrew (macOS)
brew install yt-dlp

# Verify installation
yt-dlp --version
```

## Transcript Extraction
Setup a temporary directory - IMPORTANT: Always create and use a temporary directory for downloaded files to avoid cluttering the repository:

```bash
# Create temporary directory for this analysis
ANALYSIS_DIR=$(mktemp -d)
echo "Using temporary directory: $ANALYSIS_DIR"
```

Download transcript using `yt-dlp` to extract subtitles/transcripts to the temporary directory:

```bash
# Download transcript only (no video)
yt-dlp --skip-download --write-auto-sub --sub-format vtt --output "$ANALYSIS_DIR/transcript.%(ext)s" URL

# Or get manually created subtitles if available (higher quality)
yt-dlp --skip-download --write-sub --sub-lang en --sub-format vtt --output "$ANALYSIS_DIR/transcript.%(ext)s" URL

# Get video metadata for context
yt-dlp --skip-download --print-json URL > "$ANALYSIS_DIR/metadata.json"
```

### Handle Long Transcripts
For transcripts exceeding 8,000 tokens (roughly 6,000 words or 45+ minutes):

1. Split into logical chunks based on timestamp or topic breaks.
2. Generate a summary for each chunk focusing on key concepts.
3. Create an overall synthesis connecting themes to the user's question.
4. Reference specific timestamps for detailed sections.

For shorter transcripts, analyze directly without chunking.

## Analysis Approach
When analyzing with respect to a project or question:
1. Extract the video's core concepts and techniques.
2. Identify patterns, architectures, or approaches discussed.
3. Compare with the current project's implementation.
4. Highlight relevant insights, differences, and potential applications.