---
name: markdown-video
description: Use this skill when you need to convert Deckset-format markdown slides with speaker notes into a presentation video with TTS narration.
---

# Skill body

Convert markdown slides to presentation video with AI-generated visuals and TTS audio narration.

## When to Use This Skill

Activate this skill when the user:
- Asks to create a video from markdown slides
- Requests to convert a presentation to MP4 format
- Wants to generate a narrated video from slides
- Needs automated slide-to-video conversion

## Key Features

- **Gemini AI-generated visuals**: High-quality slide images with full emoji and Korean support
- **OpenAI TTS narration**: Natural voice from speaker notes
- **Delta updates**: Only regenerates changed slides (saves time and API costs)
- **Multiple visual styles**: technical-diagram, professional, vibrant-cartoon, watercolor

## Input Requirements

- **Markdown file** with speaker notes marked with `^` prefix
- **GEMINI_API_KEY** environment variable for image generation
- **OPENAI_API_KEY** environment variable for TTS audio

## Output Specifications

- **MP4 video**: 1920x1080 (Full HD)
- **Duration**: Each slide displays for the duration of its audio narration
- **File naming**: `{input_filename}.mp4`

## Workflow

### Step 1: Generate Audio Files

```bash
cd "{slides_directory}"
python /path/to/generate_audio.py "{slides_filename}" --output-dir "audio"
```

**Delta update**: Only regenerates audio for slides with changed speaker notes.
- Use `--force` to regenerate all audio files

**Output**:
- `audio/slide_0.mp3`, `slide_1.mp3`, ... (0-indexed)
- Cache file: `audio/.audio_cache.json`

### Step 2: Generate Slide Images with Gemini

```bash
cd "{slides_directory}"
python /path/to/create_slides_gemini.py "{slides_filename}" \
  --output-dir "slides-gemini" \
  --style "technical-diagram" \
  --auto-approve
```

**Delta update**: Only regenerates images for slides with changed content.
- Use `--force` to regenerate all slide images

**Style Options**:

| Style | Description | Best For |
|-------|-------------|----------|
| `technical-diagram` | Clean lines, infographic icons, muted blue/gray | Technical, education |
| `professional` | Minimalist, geometric shapes | Corporate, formal |
| `vibrant-cartoon` | Bright colors, playful design | Creative, informal |
| `watercolor` | Soft, artistic look | Artistic presentations |