---
name: openai-image-gen
description: Use this skill to batch-generate images via the OpenAI Images API with structured prompts and an HTML gallery.
---

# OpenAI Image Gen

Generate a handful of “random but structured” prompts and render them via the OpenAI Images API.

## Setup

- Requires environment variable: `OPENAI_API_KEY`
- Ensure Python 3 is installed.

## Run

From any directory (outputs to `~/Projects/tmp/...` when present; else `./tmp/...`):

```bash
python3 {baseDir}/scripts/gen.py
open ~/Projects/tmp/openai-image-gen-*/index.html  # if ~/Projects/tmp exists; else ./tmp/...
```

## Useful Flags

### For GPT Image Models

```bash
python3 {baseDir}/scripts/gen.py --count 16 --model gpt-image-1
python3 {baseDir}/scripts/gen.py --prompt "ultra-detailed studio photo of a lobster astronaut" --count 4
python3 {baseDir}/scripts/gen.py --size 1536x1024 --quality high --out-dir ./out/images
python3 {baseDir}/scripts/gen.py --model gpt-image-1.5 --background transparent --output-format webp
```

### For DALL-E Models

```bash
# DALL-E 3 (note: count is automatically limited to 1)
python3 {baseDir}/scripts/gen.py --model dall-e-3 --quality hd --size 1792x1024 --style vivid
python3 {baseDir}/scripts/gen.py --model dall-e-3 --style natural --prompt "serene mountain landscape"

# DALL-E 2
python3 {baseDir}/scripts/gen.py --model dall-e-2 --size 512x512 --count 4
```

## Model-Specific Parameters

Different models support different parameter values. The script automatically selects appropriate defaults based on the model.

### Size Options

- **GPT Image Models**: `1024x1024`, `1536x1024` (landscape), `1024x1536` (portrait), or `auto` (default: `1024x1024`)
- **DALL-E 3**: `1024x1024`, `1792x1024`, or `1024x1792` (default: `1024x1024`)
- **DALL-E 2**: `256x256`, `512x512`, or `1024x1024` (default: `1024x1024`)

### Quality Options

- **GPT Image Models**: `auto`, `high`, `medium`, or `low` (default: `high`)
- **DALL-E 3**: `hd` or `standard` (default: `standard`)
- **DALL-E 2**: `standard` only (default: `standard`)

### Additional Notes

- DALL-E 3 only supports generating 1 image at a time (`n=1`).
- GPT image models support additional parameters like `--background` and `--output-format`.