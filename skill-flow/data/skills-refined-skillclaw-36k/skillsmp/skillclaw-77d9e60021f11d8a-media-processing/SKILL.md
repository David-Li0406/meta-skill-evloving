---
name: media-processing
description: Use this skill when you need to process multimedia files, including video, audio, and images, using FFmpeg, ImageMagick, and RMBG for various tasks like encoding, conversion, and background removal.
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
ffmpeg -i input.mkv -c copy output.mp4
ffmpeg -i input.avi -c:v libx264 -crf 22 -c:a aac output.mp4

# Video: Extract audio
ffmpeg -i video.mp4 -vn -c:a copy audio.m4a

# Image: Convert/resize
magick input.png output.jpg
magick input.jpg -resize 800x600 output.jpg

# Image: Batch resize
mogrify -resize 800x -quality 85 *.jpg

# Background removal
rmbg input.jpg                          # Basic (modnet)
rmbg input.jpg -m briaai -o output.png  # High quality
rmbg input.jpg -m u2netp -o output.png  # Fast
```

## Key Parameters

**FFmpeg:**
- `-c:v libx264` - H.264 codec
- `-crf 22` - Quality (0-51, lower=better)
- `-preset slow` - Speed/compression balance
- `-c:a aac` - Audio codec

**ImageMagick:**
- `800x600` - Fit within (maintains aspect)
- `800x600^`