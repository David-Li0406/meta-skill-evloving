---
name: video-generation
description: Generate videos using Google Veo 3.1 API with presets, extensions, and cost controls
allowed-tools:
  - Bash
  - Read
metadata:
  author: erikb
  version: 1.0.0
  category: creative
  created: 2026-01-18
---

# Video Generation - Google Veo 3.1

Generate high-quality videos using Google's Veo 3.1 API with full parameter control, presets, and video extension capabilities.

## Quick Start

```bash
# Basic generation (fast model, 720p)
bun run "${CLAUDE_PLUGIN_ROOT}/tools/Generate.ts" \
  --prompt "A cat walking on a beach at sunset" \
  --duration 8 \
  --aspect-ratio 16:9 \
  --output ~/Downloads/cat.mp4

# With preset
bun run "${CLAUDE_PLUGIN_ROOT}/tools/Generate.ts" \
  --prompt "Drone shot of coastal highway" \
  --duration 8 \
  --aspect-ratio 16:9 \
  --preset cinematic \
  --output ~/Downloads/highway.mp4
```

## Interactive Command

Use `/video` for guided video generation:
```
/video "A sunset over mountains"
/video --preset cinematic
/video
```

## Presets

| Preset | Description | Default Aspect |
|--------|-------------|----------------|
| cinematic | Film-quality, 24fps, shallow DOF | Any |
| vertical-social | 9:16 punchy social style, 30fps | 9:16 |
| product-demo | Clean studio lighting | Any |
| documentary | Nature documentary style | Any |

## Parameters

| Flag | Values | Notes |
|------|--------|-------|
| --prompt | text | Required. Max 1024 tokens |
| --duration | 4, 6, 8 | Seconds per clip |
| --aspect-ratio | 16:9, 9:16, 1:1 | Required |
| --output | path | Output .mp4 file |
| --resolution | 720p, 1080p | 1080p only for 8s |
| --speed | fast, standard | Standard is 2.6x more expensive |
| --preset | name | Apply style preset |
| --negative-prompt | text | Things to avoid |
| --reference-image | path | Up to 3 reference images |
| --seed | number | For reproducibility |

## Cost

| Model | Cost/Second | 8s Clip |
|-------|-------------|---------|
| Fast | $0.15 | $1.20 |
| Standard | $0.40 | $3.20 |

Standard mode requires `--confirm-cost` flag.

## Video Extension

Extend videos in 7-second increments (up to 148s total):

```bash
# Generate base clip
bun run "${CLAUDE_PLUGIN_ROOT}/tools/Generate.ts" \
  --prompt "Scene opening" \
  --duration 8 \
  --aspect-ratio 16:9 \
  --output base.mp4

# Extend with continuation prompt
bun run "${CLAUDE_PLUGIN_ROOT}/tools/Generate.ts" \
  --extend base.mp4 \
  --prompt "Continue as sun sets" \
  --output extended.mp4
```

Extension costs: $1.05 (fast) or $2.80 (standard) per 7s extension.

## Query Operations

```bash
# List presets
bun run "${CLAUDE_PLUGIN_ROOT}/tools/Generate.ts" --list-presets

# Show preset details
bun run "${CLAUDE_PLUGIN_ROOT}/tools/Generate.ts" --show-preset cinematic

# Estimate cost
bun run "${CLAUDE_PLUGIN_ROOT}/tools/Generate.ts" \
  --prompt "test" --duration 8 --aspect-ratio 16:9 --dry-run

# Preview final prompt (with preset applied)
bun run "${CLAUDE_PLUGIN_ROOT}/tools/Generate.ts" \
  --prompt "A mountain scene" --preset cinematic --prompt-only

# Check operation status
bun run "${CLAUDE_PLUGIN_ROOT}/tools/Generate.ts" --status op_abc123
```

## Environment

Requires `GOOGLE_API_KEY` in `~/.claude/.env`

## See Also

- `references/prompting.md` - 6-part prompt formula guide
- `${CLAUDE_PLUGIN_ROOT}/tools/Presets.json` - Customizable presets
