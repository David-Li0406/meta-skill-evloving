---
name: image-generation
description: Use this skill for generating images via official OpenAI and Google APIs, supporting various prompts, aspect ratios, and quality presets.
---

# Image Generation (AI SDK)

Official API-based image generation using OpenAI and Google providers. Supports text-to-image, reference images, aspect ratios, and quality presets.

## Script Directory

**Agent Execution**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`.
2. Script path = `${SKILL_DIR}/scripts/main.ts`.

## Quick Start

```bash
# Basic generation (auto-detect provider)
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "<prompt_text>" --image <output_image_path>

# With aspect ratio
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "<prompt_text>" --image <output_image_path> --ar <aspect_ratio>

# High quality (2k)
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "<prompt_text>" --image <output_image_path> --quality 2k

# Specific provider
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "<prompt_text>" --image <output_image_path> --provider <provider_name>

# From prompt files
npx -y bun ${SKILL_DIR}/scripts/main.ts --promptfiles <file1> <file2> --image <output_image_path>

# With reference images (Google multimodal only)
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "<prompt_text>" --image <output_image_path> --ref <reference_image_path>
```

## Options

| Option | Description |
|--------|-------------|
| `--prompt <text>`, `-p` | Prompt text |
| `--promptfiles <files...>` | Read prompt from files (concatenated) |
| `--image <path>` | Output image path (required) |
| `--provider google\|openai` | Force provider (default: google) |
| `--model <id>`, `-m` | Model ID |
| `--ar <ratio>` | Aspect ratio (e.g., `16:9`, `1:1`, `4:3`) |
| `--size <WxH>` | Size (e.g., `1024x1024`) |
| `--quality normal\|2k` | Quality preset (default: normal) |
| `--ref <files...>` | Reference images (Google multimodal only) |
| `--n <count>` | Number of images |
| `--json` | JSON output |
| `--help`, `-h` | Show help |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |
| `GOOGLE_API_KEY` | Google API key |
| `OPENAI_IMAGE_MODEL` | OpenAI model override |
| `GOOGLE_IMAGE_MODEL` | Google model override |
| `OPENAI_BASE_URL` | Custom OpenAI endpoint |
| `GOOGLE_BASE_URL` | Custom Google endpoint |

**Load Priority**: CLI args > env vars > `<cwd>/.baoyu-skills/.env` > `~/.baoyu-skills/.env`

## Provider Selection

1. If `--provider` specified → use it.
2. If only one API key available → use that provider.
3. If both available → default to Google.

## Quality Presets

| Preset | Resolution | Use Case |
|--------|------------|----------|
| `normal` | ~1024px | Covers, illustrations |
| `2k` | ~2048px | Infographics, slides |

## Aspect Ratios

Supported: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `2.35:1`.

## Error Handling

- Missing API key → error with setup instructions.
- Generation failure → auto-retry once.
- Invalid aspect ratio → warning, proceed with default.
- Reference images with non-multimodal model → warning, ignore refs.

## Extension Support

Custom configurations via EXTEND.md. Check paths (priority order):
1. `.baoyu-skills/image-gen/EXTEND.md` (project)
2. `~/.baoyu-skills/image-gen/EXTEND.md` (user)

If found, load before workflow. Extension content overrides defaults.