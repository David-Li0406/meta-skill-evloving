---
name: media-processing
description: Use this skill to process multimedia files, including video, audio, and images, with FFmpeg, ImageMagick, and RMBG for various tasks such as encoding, conversion, filtering, and background removal.
---

# Media Processing Skill

Process video, audio, and images using FFmpeg, ImageMagick, and RMBG CLI tools.

## Tool Selection

| Task | Tool | Reason |
|------|------|--------|
| Video encoding/conversion | FFmpeg | Native codec support, streaming |
| Audio extraction/conversion | FFmpeg | Direct stream manipulation |
| Image resize/effects | ImageMagick | Optimized for still images |
| Background removal | RMBG | AI-powered, local processing |
| Batch images | ImageMagick | mogrify for in-place edits |
| Video thumbnails | FFmpeg | Frame extraction built-in |
| GIF creation | FFmpeg/ImageMagick | FFmpeg for video, ImageMagick for images |

## Installation

```bash
# macOS
brew install ffmpeg imagemagick
npm install -g rmbg-cli

# Ubuntu/Debian
sudo apt-get install ffmpeg imagemagick
npm install -g rmbg-cli

# Verify
ffmpeg -version && magick -version && rmbg --version
```

## Essential Commands

```bash
# Video: Convert/re-encode
ffmpeg -i <input_video> -c copy <output_video>
ffmpeg -i <input_video> -c:v libx264 -crf 22 -c:a aac <output_video>

# Video: Extract audio
ffmpeg -i <input_video> -vn -c:a copy <output_audio>

# Image: Convert/resize
magick <input_image> <output_image>
magick <input_image> -resize <width>x<height> <output_image>

# Image: Batch resize
mogrify -resize <width>x -quality <quality> *.jpg

# Background removal
rmbg <input_image>                          # Basic (modnet)
rmbg <input_image> -m briaai -o <output_image>  # High quality
rmbg <input_image> -m u2netp -o <output_image>  # Fast
```

## Key Parameters

**FFmpeg:**
- `-c:v libx264` - H.264 codec
- `-crf 22` - Quality (0-51, lower=better)
- `-preset slow` - Speed/compression balance
- `-c:a aac` - Audio codec

**ImageMagick:**
- `<width>x<height>` - Fit within (maintains aspect)
- `<width>x<height>^` - Fill (may crop)
- `-quality <quality>` - JPEG quality
- `-strip` - Remove metadata

**RMBG:**
- `-m briaai` - High quality model
- `-m u2netp` - Fast model
- `-r 4096` - Max resolution

## References

Detailed guides in `references/`:
- `ffmpeg-encoding.md` - Codecs, quality, hardware acceleration
- `ffmpeg-streaming.md` - HLS/DASH, live streaming
- `ffmpeg-filters.md` - Filters, complex filtergraphs
- `imagemagick-editing.md` - Effects, transformations
- `imagemagick-batch.md` - Batch processing, parallel ops
- `rmbg-background-removal.md` - AI models, CLI usage
- `common-workflows.md` - Video optimization, responsive images, GIF creation
- `troubleshooting.md` - Error fixes, performance tips
- `format-compatibility.md` - Format support, codec recommendations

## Task Planning Notes

- Always plan and break many small todo tasks.
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed.