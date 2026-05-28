---
name: api-image-generation
description: Use this skill when you need to generate images using official OpenAI and Google APIs via AI SDK, supporting various features like text-to-image, aspect ratios, and quality presets.
---

# Image Generation (AI SDK)

Official API-based image generation using OpenAI and Google providers.

## Script Directory

**Agent Execution**:
1. `SKILL_DIR` = this SKILL.md file's directory
2. Script path = `${SKILL_DIR}/scripts/main.ts`

## Preferences (EXTEND.md)

Use Bash to check for the existence of `EXTEND.md` (priority order):

```bash
# Check project-level first
test -f .baoyu-skills/api-image-generation/EXTEND.md && echo "project"

# Then user-level (cross-platform: $HOME works on macOS/Linux/WSL)
test -f "$HOME/.baoyu-skills/api-image-generation/EXTEND.md" && echo "user"
```

┌──────────────────────────────────────────────────┬───────────────────┐
│                       Path                       │     Location      │
├──────────────────────────────────────────────────┼───────────────────┤
│ .baoyu-skills/api-image-generation/EXTEND.md     │ Project directory │
├──────────────────────────────────────────────────┼───────────────────┤
│ $HOME/.baoyu-skills/api-image-generation/EXTEND.md │ User home         │
└──────────────────────────────────────────────────┴───────────────────┘

┌───────────┬───────────────────────────────────────────────────────────────────────────┐
│  Result   │                                  Action                                   │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Found     │ Read, parse, apply settings                                               │
├───────────┼───────────────────────────────────────────────────────────────────────────┤
│ Not found │ Use defaults                                                              │
└───────────┴───────────────────────────────────────────────────────────────────────────┘

**EXTEND.md Supports**: Default provider | Default quality | Default aspect ratio

## Usage

```bash
# Basic generation (auto-detect provider)
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image cat.png

# With aspect ratio
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A landscape" --image landscape.png --ar 16:9

# High quality (2k)
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image cat.png --quality 2k

# Specific provider
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image cat.png --provider openai

# From prompt files
npx -y bun ${SKILL_DIR}/scripts/main.ts --promptfiles system.md content.md --image out.png

# With reference images (Google multimodal only)
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "Make it blue" --image out.png --ref source.png
```

## Commands

### Basic Image Generation

```bash
# Generate with prompt
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A sunset over mountains" --image sunset.png

# Shorthand
npx -y bun ${SKILL_DIR}/scripts/main.ts -p "A cute robot" --image robot.png
```

### Aspect Ratios

```bash
# Common ratios: 1:1, 16:9, 9:16, 4:3, 3:4, 2.35:1
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A portrait" --image portrait.png --ar 3:4

# Or specify exact size
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "Banner" --image banner.png --size 1792x1024
```

### Reference Images (Google Multimodal)

```bash
# Image editing with reference
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "Make it blue" --image blue.png --ref original.png

# Multiple references
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "Combine these styles" --image out.png --ref a.png b.png
```

### Quality Presets

```bash
# Normal quality (default)
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A high-quality image" --image high_quality.png --quality normal
```