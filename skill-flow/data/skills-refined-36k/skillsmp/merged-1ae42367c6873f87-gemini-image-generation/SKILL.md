---
name: gemini-image-generation
description: Use this skill to generate images from text prompts or reference images using Google's Gemini AI, suitable for creating visual content like game assets, concept art, and promotional images.
---

# Gemini Image Generation

## Overview

This skill enables image generation using Google's Gemini AI, supporting both text-to-image and image-to-image capabilities. It provides a reusable script that handles API authentication, request formatting, response processing, and automatic image saving with error handling.

## When to Use This Skill

Use this skill when the user requests:
- Creating or generating images from text descriptions
- Visualizing concepts, scenes, or objects through AI-generated imagery
- Producing multiple variations of an image concept
- Creating images with specific aspect ratios or quality levels
- Applying style transfer using reference images

**Example requests:**
- "Generate an image of a sunset over mountains"
- "Create a logo concept showing a geometric bird"
- "Make me an image of a futuristic city at night in 16:9 ratio"
- "Generate 3 variations of a robot painting artwork"
- "Create a character design with a whimsical style"

## Configuration

### API Key Setup

The Gemini API requires an API key for authentication. Obtain a key from [Google AI Studio](https://ai.google.dev/).

**Recommended approach:** Store the API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"  # Unix
# or
$env:GEMINI_API_KEY = "your-api-key"  # PowerShell
```

### Python Dependencies

The script requires these Python packages:
- `requests` - HTTP client for API calls
- `Pillow` - Image processing library

These should be installed in a virtual environment:

```bash
# Navigate to scripts directory
cd scripts

# Create virtual environment
python3 -m venv venv

# Install dependencies
./venv/bin/pip install -r requirements.txt  # Unix
# or
.\venv\Scripts\pip install -r requirements.txt  # Windows

# Activate the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Generating Images

### Basic Usage

To generate a single image with default settings:

```bash
python generate.py --prompt "your prompt here" --output output_image.png
```

### With Reference Image (Style Transfer)

To generate an image using a reference for style:

```bash
python generate.py --prompt "your prompt here" --reference reference_image.png --output output_image.png
```

### Advanced Options

#### Model Selection

Choose from different quality/speed tiers:

```bash
# Fast generation (default)
--model imagen-4.0-fast-generate-001

# Standard generation
--model imagen-4.0-generate-001

# Ultra generation
--model imagen-4.0-ultra-generate-001
```

#### Aspect Ratios

Generate images in different dimensions:

```bash
--aspect-ratio 1:1  # Square
--aspect-ratio 3:4  # Portrait
--aspect-ratio 4:3  # Landscape
--aspect-ratio 16:9 # Widescreen
```

#### Multiple Images

Generate up to 4 variations in a single request:

```bash
--num 4
```

#### Output Directory

Specify where to save generated images:

```bash
--output ./generated_images
```

### Complete Examples

**Generate a high-quality landscape image:**
```bash
python generate.py \
  --prompt "Majestic mountain range at golden hour with dramatic clouds" \
  --output ./landscapes/landscape.png \
  --model imagen-4.0-ultra-generate-001 \
  --aspect-ratio 16:9
```

**Create multiple logo variations:**
```bash
python generate.py \
  --prompt "Minimalist geometric logo for tech startup, blue and white" \
  --num 4 \
  --aspect-ratio 1:1 \
  --output ./logo_concepts
```

**Quick social media graphic:**
```bash
python generate.py \
  --prompt "Abstract colorful pattern for social media background" \
  --aspect-ratio 9:16 \
  --output ./social_media/social_media_background.png
```

## Workflow Integration

When a user requests image generation:

1. **Extract the prompt** from the user's request.
2. **Determine parameters** based on context:
   - Aspect ratio (square for logos, 16:9 for presentations, etc.)
   - Number of variations (if user wants options)
   - Quality tier (ultra for final outputs, fast for iteration)
3. **Invoke the script** with appropriate parameters.
4. **Show the generated images** to the user and provide file paths.
5. **Iterate if needed** with refined prompts or different parameters.

## Best Practices

### Prompt Engineering

- **Be specific and descriptive:** Include details about style, lighting, composition, colors.
- **Specify art style if desired:** "digital art", "oil painting", "photorealistic", "minimalist".
- **Mention important elements:** Objects, subjects, background, atmosphere.
- **Include quality keywords:** "high detail", "professional", "award-winning".

**Example good prompt:**
> "A serene Japanese garden with cherry blossoms in full bloom, koi pond in foreground, traditional stone lantern, soft morning light, photorealistic style, high detail."

### Error Handling

The script handles common errors:
- Invalid API keys → Check API key configuration.
- Network timeouts → Verify internet connection, retry request.
- Rate limiting → Wait and retry, consider reducing simultaneous requests.
- Invalid parameters → Review model name, aspect ratio, and num_images values.

## Output Format

Generated images are saved as PNG files with:
- **Naming convention:** `gemini_image_YYYYMMDD_HHMMSS_N.png`
- **Timestamp:** Ensures unique filenames across runs.
- **Sequential numbering:** When generating multiple images.
- **SynthID watermark:** Automatically embedded by Imagen API.

## Resources

### scripts/generate.py

The main image generation script that handles:
- API authentication and request formatting.
- Base64 image decoding and PIL processing.
- Automatic file saving with timestamps.
- Comprehensive error handling and user feedback.
- Command-line interface with all customization options.

Invoke directly from the command line or integrate into larger workflows.