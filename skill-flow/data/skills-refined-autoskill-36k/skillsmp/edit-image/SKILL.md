---
name: Edit Image
description: This skill should be used when the user asks to "edit an image", "modify a photo", "inpaint", "outpaint", "extend an image", "replace object in image", "add element to image", or needs AI-powered image editing with masks.
---

# Edit Image

Edit images using Gemini's imagen-3.0 editor (inpainting/outpainting).

## When to Use

Use this skill when the user asks to:
- Edit part of an image (inpainting)
- Extend an image beyond its borders (outpainting)
- Replace objects or regions in an image
- Add elements to an existing image

## Usage

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/edit-image && bun run scripts/edit.ts <input-image> "edit prompt" [options]
```

### Options

- `--mask <path>` - Mask image (white = edit area, black = keep)
- `--mode <inpaint|outpaint>` - Edit mode
- `--format <png|jpeg|webp>` - Output format
- `--quality <n>` - JPEG quality (1-100)
- `--negative <prompt>` - Negative prompt
- `--count <n>` - Number of variations
- `--guidance <n>` - Guidance scale
- `--seed <n>` - Random seed
- `--output <path>` - Output path

### Examples

```bash
# Inpaint with mask
cd ${CLAUDE_PLUGIN_ROOT}/skills/edit-image && bun run scripts/edit.ts photo.jpg "add a sunset sky" --mask sky_mask.png --mode inpaint

# Outpaint to extend image
cd ${CLAUDE_PLUGIN_ROOT}/skills/edit-image && bun run scripts/edit.ts photo.jpg "extend the landscape" --mode outpaint

# Replace object with multiple variations
cd ${CLAUDE_PLUGIN_ROOT}/skills/edit-image && bun run scripts/edit.ts scene.jpg "replace the car with a bicycle" --mask car_mask.png --count 3
```

## Model

Uses `imagen-3.0-capability-001` with editing configuration.
