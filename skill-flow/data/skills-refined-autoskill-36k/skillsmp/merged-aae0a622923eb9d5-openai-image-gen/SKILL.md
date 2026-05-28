---
name: openai-image-gen
description: Use this skill to batch-generate images via the OpenAI Images API with structured prompts and an HTML gallery.
---

# OpenAI Image Gen

Generate a set of structured prompts and render them using the OpenAI Images API.

## Setup

- Requires environment variable: `OPENAI_API_KEY`

## Run

From any directory (outputs to `~/Projects/tmp/...` if it exists; otherwise, `./tmp/...`):

```bash
python3 {baseDir}/scripts/gen.py
open ~/Projects/tmp/openai-image-gen-*/index.html
```

## Useful Flags

### For GPT Image Models

```bash
python3 {baseDir}/scripts/gen.py --count <number> --model <model_name>
python3 {baseDir}/scripts/gen.py --prompt "<your_prompt>" --count <number>
python3 {baseDir}/scripts/gen.py --size <width>x<height> --quality <quality_level> --out-dir <output_directory>
python3 {baseDir}/scripts/gen.py --model gpt-image-1.5 --background <background_option> --output-format <format>
```

### For DALL-E Models

```bash
# DALL-E 3 (count is limited to 1)
python3 {baseDir}/scripts/gen.py --model dall-e-3 --quality <quality_level> --size <width>x<height> --style <style_option>
python3 {baseDir}/scripts/gen.py --model dall-e-2 --size <width>x<height> --count <number>
```

## Model-Specific Parameters

### Size Options

- **GPT Image Models**: `1024x1024`, `1536x1024`, `1024x1536`, or `auto` (default: `1024x1024`)
- **DALL-E 3**: `1024x1024`, `1792x1024`, or `1024x1792` (default: `1024x1024`)
- **DALL-E 2**: `256x256`, `512x512`, or `1024x1024` (default: `1024x1024`)

### Quality Options

- **GPT Image Models**: `auto`, `high`, `medium`, or `low` (default: `high`)
- **DALL-E 3**: `hd` or `standard` (default: `standard`)
- **DALL-E 2**: `standard` only (default: `standard`)

### Additional Parameters

- **DALL-E 3**: Only supports generating 1 image at a time.
- **GPT Image Models**: Supports `--background` (`transparent`, `opaque`, or `auto`) and `--output-format` (`png`, `jpeg`, or `webp`).

## Output

- Generated images in `*.png`, `*.jpeg`, or `*.webp` format (depends on model and `--output-format`)
- `prompts.json` (mapping of prompts to files)
- `index.html` (thumbnail gallery)