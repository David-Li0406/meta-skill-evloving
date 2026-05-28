---
name: nanobanana-skill
description: Use this skill when you need to generate or edit images using the Google Gemini API via the nanobanana tool.
---

# Nanobanana Image Generation Skill

Generate or edit images using the Google Gemini API through the nanobanana tool.

## Requirements

1. **GEMINI_API_KEY**: Must be configured in `~/.nanobanana.env` or set as an environment variable: `export GEMINI_API_KEY=<your-api-key>`.
2. **Python3 with dependent packages installed**: Install required packages using:
   ```bash
   python3 -m pip install -r ~/.codex/skills/nanobanana-skill/requirements.txt
   ```
3. **Executable**: `~/.codex/skills/nanobanana-skill/nanobanana.py`

## Instructions

### For Image Generation

1. Ask the user for:
   - What they want to create (the prompt)
   - Desired aspect ratio/size (optional, defaults to 9:16 portrait)
   - Output filename (optional, auto-generates UUID if not specified)
   - Model preference (optional, defaults to `gemini-3-pro-image-preview`)
   - Resolution (optional, defaults to 1K)

2. Run the nanobanana script with appropriate parameters:
   ```bash
   python3 ~/.codex/skills/nanobanana-skill/nanobanana.py --prompt "description of image" --output "filename.png"
   ```

3. Show the user the saved image path when complete.

### For Image Editing

1. Ask the user for:
   - Input image file(s) to edit
   - What changes they want (the prompt)
   - Output filename (optional)

2. Run with input images:
   ```bash
   python3 ~/.codex/skills/nanobanana-skill/nanobanana.py --prompt "editing instructions" --input image1.png image2.png --output "edited.png"
   ```

## Available Options

### Aspect Ratios (--size)

- `1024x1024` (1:1) - Square
- `832x1248` (2:3) - Portrait
- `1248x832` (3:2) - Landscape
- `864x1184` (3:4) - Portrait
- `1184x864` (4:3) - Landscape
- `896x1152` (4:5) - Portrait
- `1152x896` (5:4) - Landscape
- `768x1344` (9:16) - Portrait (default)
- `1344x768` (16:9) - Landscape
- `1536x672` (21:9) - Ultra-wide

### Models (--model)

- `gemini-3-pro-image-preview` (default) - Higher quality
- `gemini-2.5-flash-image` - Faster generation

### Resolution (--resolution)

- `1K` (default)
- `2K`
- `4K`