---
name: image-generation-and-editing
description: Use this skill when you need to generate new images or edit existing ones using OpenAI's GPT Image model, including selective editing with masks and combining multiple images.
---

# Image Generation & Editing

Generate new images or edit existing ones using OpenAI's GPT Image model.

## Image Generation

- **Generation**: Create images based on a text prompt using the Responses API with the image_generation tool.

### Usage

Run the script using absolute path (do NOT cd to skill directory first):

**Generate new image:**
```bash
uv run <path-to-script>/generate_image.py --prompt "<your image description>" --filename "<output-name.png>" [--quality low|medium|high] [--size 1024x1024|1024x1536|1536x1024|auto] [--background transparent|opaque|auto] [--api-key <KEY>]
```

## Image Editing

Edit existing images using the Image API for reliable results, including options for full image edits and precise inpainting with masks.

### Editing Modes

1. **Full Image Edit (without mask)**:
   - Use when the user wants to modify an existing image without specifying exact regions.
   - Command:
   ```bash
   uv run <path-to-script>/generate_image.py --prompt "<editing instructions>" --filename "<output-name.png>" --input-image "<path/to/input.png>" [--size 1024x1024|1024x1536|1536x1024|auto] [--api-key <KEY>]
   ```

2. **Precise Inpainting (with mask)**:
   - Use when the user wants to edit specific regions of an image.
   - Command:
   ```bash
   uv run <path-to-script>/generate_image.py --prompt "<what to put in masked area>" --filename "<output-name.png>" --input-image "<path/to/input.png>" --mask "<path/to/mask.png>" [--size 1024x1024|1024x1536|1536x1024|auto] [--api-key <KEY>]
   ```

### Important Notes

- Always run from the user's current working directory to save images where the user is working.
- The script checks for the API key in the following order:
  1. `--api-key` argument
  2. `OPENAI_API_KEY` environment variable

## Parameters

### Quality Options
- **low** - Fastest generation, lower quality
- **medium** (default) - Balanced quality and speed
- **high** - Best quality, slower generation

### Size Options
- **1024x1024** (default) - Square format
- **1024x1536** - Portrait format
- **1536x1024** - Landscape format
- **auto** - Let the model decide based on prompt

### Background Options (generation only)
- **auto** (default) - Model decides
- **transparent** - Transparent background (PNG/WebP output)
- **opaque** - Solid background

## Filename Generation

Generate filenames with the pattern: `yyyy-mm-dd-hh-mm-ss-name.png`

**Format:** `{timestamp}-{descriptive-name}.png`
- Timestamp: Current date/time in format `yyyy-mm-dd-hh-mm-ss` (24-hour format)
- Name: Descriptive lowercase text with hyphens

## Common Editing Tasks

- Add/remove elements
- Change style
- Adjust colors
- Replace backgrounds

## Output

- Saves PNG to the current directory (or specified path if filename includes directory).
- The script outputs the full path to the generated image.

## Examples

**Generate new image:**
```bash
uv run <path-to-script>/generate_image.py --prompt "A serene Japanese garden with cherry blossoms" --filename "2025-12-17-14-23-05-japanese-garden.png" --quality high --size 1536x1024
```

**Edit existing image (full image):**
```bash
uv run <path-to-script>/generate_image.py --prompt "make the sky more dramatic with storm clouds" --filename "2025-12-17-14-27-00-dramatic-sky.png" --input-image "original-photo.jpg"
```

**Edit with mask (inpainting):**
```bash
uv run <path-to-script>/generate_image.py --prompt "a flamingo swimming" --filename "2025-12-17-14-30-00-lounge-flamingo.png" --input-image "lounge.png" --mask "mask.png"
```