---
name: generate-image
description: Use this skill when you need to generate or edit images using AI models like FLUX and Gemini for various visual content, excluding technical diagrams.
---

# Generate Image

Generate and edit high-quality images using OpenRouter's image generation models including FLUX.2 Pro and Gemini 3 Pro.

## When to Use This Skill

**Use generate-image for:**
- Photos and photorealistic images
- Artistic illustrations and artwork
- Concept art and visual concepts
- Visual assets for presentations or documents
- Image editing and modifications
- Any general-purpose image generation needs

**Use scientific-schematics instead for:**
- Flowcharts and process diagrams
- Circuit diagrams and electrical schematics
- Biological pathways and signaling cascades
- System architecture diagrams
- CONSORT diagrams and methodology flowcharts
- Any technical/schematic diagrams

## Quick Start

Use the `scripts/generate_image.py` script to generate or edit images:

```bash
# Generate a new image
python scripts/generate_image.py "A beautiful sunset over mountains"

# Edit an existing image
python scripts/generate_image.py "Make the sky purple" --input photo.jpg
```

This generates/edits an image and saves it as `generated_image.png` in the current directory.

## API Key Setup

**CRITICAL**: The script requires an OpenRouter API key. Before running, check if the user has configured their API key:

1. Look for a `.env` file in the project directory or parent directories.
2. Check for `OPENROUTER_API_KEY=<key>` in the `.env` file.
3. If not found, inform the user they need to:
   - Create a `.env` file with `OPENROUTER_API_KEY=your-api-key-here`
   - Or set the environment variable: `export OPENROUTER_API_KEY=your-api-key-here`
   - Get an API key from: https://openrouter.ai/keys

The script will automatically detect the `.env` file and provide clear error messages if the API key is missing.

## Model Selection

**Default model**: `google/gemini-3-pro-image-preview` (high quality, recommended)

**Available models for generation and editing**:
- `google/gemini-3-pro-image-preview` - High quality, supports generation + editing
- `black-forest-labs/flux.2-pro` - Fast, high quality, supports generation + editing
- `black-forest-labs/flux.2-flex` - Fast and cheap, but not as high quality as pro