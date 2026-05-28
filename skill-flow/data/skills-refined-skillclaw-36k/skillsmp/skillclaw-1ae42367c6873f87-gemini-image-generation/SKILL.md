---
name: gemini-image-generation
description: Use this skill to generate images from text prompts or reference images using Google's Gemini Imagen API, ideal for creating visual content like game assets, concept art, and promotional images.
---

# Gemini Image Generation

## Overview

This skill enables the generation of images from text prompts or reference images using Google's Gemini Imagen API. It provides a reusable script that handles API authentication, request formatting, response processing, and automatic image saving with proper error handling.

## When to Use This Skill

Use this skill when the user requests:
- Creating or generating images from text descriptions
- Visualizing concepts, scenes, or objects through AI-generated imagery
- Producing multiple variations of an image concept
- Creating images with specific aspect ratios or quality levels
- Generating images with style transfer from reference images

**Example requests:**
- "Generate an image of a sunset over mountains"
- "Create a logo concept showing a geometric bird"
- "Make me an image of a futuristic city at night in 16:9 ratio"
- "Generate 3 variations of a robot painting artwork"
- "Create a serene mountain landscape at sunset"
- "Generate a winter version of the landscape using a reference image"

## Configuration

### API Key Setup

The Gemini API requires an API key for authentication. Obtain a key from [Google AI Studio](https://ai.google.dev/).

**Recommended approach:** Store the API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Alternatively, pass the key directly when invoking the script (less secure for shared environments).

### Python Dependencies

The script requires these Python packages:
- `requests` - HTTP client for API calls
- `Pillow` - Image processing library

These are included in the project's shared virtual environment. Activate it before running:

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Generating Images

### Basic Usage

To generate a single image with default settings:

```bash
python scripts/generate_image.py --prompt "your prompt here" --api-key $GEMINI_API_KEY
```

The script will:
1. Send the prompt to the Gemini Imagen API
2. Receive and decode the generated image(s)
3. Save images with timestamped filenames (e.g., `gemini_image_20231123_142530_1.png`)
4. Display progress and file paths

### Advanced Options

#### Model Selection

Choose from three quality/speed tiers:

```bash
# Fast generation (default) - quickest, good quality
--model imagen-4.0-fast-generate-001

# Standard generation - balanced speed and quality
--model imagen-4.0-standard-generate-001

# High-quality generation - best quality, slower
--model imagen-4.0-high-quality-001
```

### Image Generation with Reference

To generate an image using a reference image for style transfer:

```bash
python scripts/generate_image.py --prompt "your prompt here" --reference reference_image.png --output output_image.png --api-key $GEMINI_API_KEY
```

## Prompt Engineering Tips

For best results, structure prompts as:

```
[Subject] + [Style] + [Composition] + [Technical] + [Mood]
```

**Example for game assets:**
```
"A bio-mimetic robot with Art Nouveau brass gears and botanical vine patterns, 
centered composition on transparent background, flat vector style suitable for 
game sprite, warm golden hour lighting, whimsical and charming mood"
```

**Style keywords that work well:**
- Art styles: Art Nouveau, steampunk, Studio Ghibli, pixel art, vector illustration
- Technical: transparent background, game sprite, icon, UI element, seamless texture
- Mood: whimsical, dramatic, cozy, ethereal, vibrant

## Troubleshooting

| Error | Solution |
|-------|----------|
| API key not valid | Check GEMINI_API_KEY is set correctly |
| 403 Forbidden | API key may have IP restrictions |
| Other errors | Refer to the API documentation for further troubleshooting steps. |