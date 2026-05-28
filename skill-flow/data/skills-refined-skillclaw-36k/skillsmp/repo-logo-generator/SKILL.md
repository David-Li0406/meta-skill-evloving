---
name: repo-logo-generator
description: Generate logos for GitHub repositories via OpenRouter using Gemini with programmatic transparency conversion. Works with pixel art, vector designs, and complex multi-colored styles. Use when asked to "generate a logo", "create repo logo", or "make a project logo".
license: MIT
compatibility: python 3.8+, requires requests and pillow libraries, uses OpenRouter skill
argument-hint: "[style-preference]"
disable-model-invocation: false
user-invocable: true
metadata:
  version: "3.3.0"
---

# Repo Logo Generator

Generate professional logos with transparent backgrounds using chromakey technology:
1. **Gemini** (google/gemini-3-pro-image-preview) generates logo with green (#00FF00) background
2. **PIL** applies professional chromakey algorithm for smooth transparency

The chromakey approach eliminates "halo" artifacts around edges that occur with white background conversion. This is the same technique used in film/TV green screen compositing (hence "green screen").

## Path Resolution

The logo generation script must be resolved from the plugin cache using an absolute path. Never use relative paths.

**Dynamic resolution (recommended):**
```bash
# Find latest repo-logo-generator version
LATEST_VERSION=$(ls -1 ~/.claude/plugins/cache/claude-skills/repo-logo-generator 2>/dev/null | sort -V | tail -n 1)
LOGO_SCRIPT="$HOME/.claude/plugins/cache/claude-skills/repo-logo-generator/$LATEST_VERSION/skills/repo-logo-generator/scripts/generate_logo.py"

# Verify it exists
if [ ! -f "$LOGO_SCRIPT" ]; then
  echo "Error: repo-logo-generator plugin not found. Install via: /skills-discovery repo-logo-generator" >&2
  exit 1
fi

# Use in command
uv run --with requests --with pillow "$LOGO_SCRIPT" \
  "Your prompt here" \
  --output logo.png
```

**Important:** Always validate that the script exists before attempting to execute it. If not found, inform the user immediately and do not proceed.

## REQUIRED: Execution Checklist (MUST complete in order)

Follow these steps exactly. Do not skip steps or improvise.

- [ ] **Step 0**: Create Todo List
  - Use TodoWrite to create a todo list with these items:
    1. Validate dependencies (find script, check API key)
    2. Load configuration files (project → user → default)
    3. Read project documentation to determine type
    4. Generate logo using Gemini with chromakey background
    5. Verify logo file and properties

  This is a multi-step task requiring todo list tracking per TodoWrite guidelines.

- [ ] **Step 1**: Validate Dependencies
  - Locate latest generation script using path resolution logic above
  - Verify `SKILL_OPENROUTER_API_KEY` environment variable is set
  - If either check fails, report to user immediately and do not proceed
  - Mark "Validate dependencies" todo as completed

- [ ] **Step 2**: Load config by reading each path in order (stop at first that exists):
  1. Read `./.claude/readme-generator.json` (project config)
  2. Read `~/.claude/readme-generator.json` (user config)
  3. Read `assets/default-config.json` from this skill's directory (default)

  **IMPORTANT**: Actually READ each file path, don't just search for JSON files.
  Mark "Load configuration files" todo as completed after this step.

- [ ] **Step 3**: Check if config has `style` parameter:
  - **If YES** (user has custom settings): Use the `config.style` value AS-IS for the entire prompt. DO NOT use the template below. DO NOT enforce "no text" or "vector style" rules. The user's style setting completely overrides all defaults.
  - **If NO** (using defaults): Continue to Step 4.

  **CRITICAL: Chromakey Color Handling**
  - The `--key-color` flag MUST use `config.keyColor` (default: `#00FF00` green)
  - NEVER infer `--key-color` from background colors mentioned in the `style` text
  - The style text tells Gemini what to generate; `keyColor` tells PIL what color to remove
  - If the style mentions "white background", "magenta background", etc., IGNORE it for `--key-color`
  - Only use a non-green `--key-color` if `config.keyColor` is explicitly set in the JSON

- [ ] **Step 4**: Read project files (README, package.json, etc.) to determine project type
  Mark "Read project documentation" todo as completed after this step.

- [ ] **Step 5**: Select visual metaphor from the table below and fill the prompt template

- [ ] **Step 6**: Generate logo:
  - Gemini generates image with green (#00FF00) chromakey background
  - PIL applies chromakey algorithm for smooth transparent edges
  - Use absolute path to script (resolved in Step 1)
  - Command format:
    ```bash
    uv run --with requests --with pillow \
      "$LOGO_SCRIPT" \
      "[YOUR PROMPT HERE]" \
      --output logo.png
    ```
  Mark "Generate logo" todo as completed after this step.

- [ ] **Step 7**: Verify logo exists and is valid PNG with transparency
  Mark "Verify logo file and properties" todo as completed after this step.

## Sandbox Compatibility

On macOS, `uv run` may require `dangerouslyDisableSandbox: true` (UV accesses system APIs). Claude will retry with sandbox disabled if needed.

**Alternative:** Pre-install dependencies with `pip install requests pillow` and use `python3` directly.

## Prompt Template (MANDATORY - DO NOT MODIFY FORMAT)

You MUST construct the prompt using this EXACT template. Do not paraphrase, do not add creative flourishes, do not skip any line.

```
A {config.style} logo for {PROJECT_NAME}: {VISUAL_METAPHOR_FROM_TABLE}.
Clean vector style. Icon colors from: {config.iconColors}.
Pure bright green (#00FF00) background only. Do not use green tones anywhere in the design.
No text, no letters, no words. Single centered icon, geometric shapes, works at {config.size}.
```

**Default values** (when no config exists):
- `config.style` = `minimalist`
- `config.iconColors` = `#58a6ff, #d29922, #a371f7, #7aa2f7, #f97583` (avoid green)
- `config.size` = `64x64`
- `config.model` = `google/gemini-3-pro-image-preview`
- `config.keyColor` = `#00FF00` (green)
- `config.tolerance` = `70`

### Filled Example

For a CLI tool called "fastgrep":

```
A minimalist logo for fastgrep: A magnifying glass with speed lines forming a geometric pattern.
Clean vector style. Icon colors from: #58a6ff, #d29922, #a371f7, #7aa2f7, #f97583.
Pure bright green (#00FF00) background only. Do not use green tones anywhere in the design.
No text, no letters, no words. Single centered icon, geometric shapes, works at 64x64.
```

## Visual Metaphors by Project Type (MUST use this table)

Select the metaphor that matches the project type. Do NOT invent alternatives.

| Project Type | Visual Metaphor |
|--------------|-----------------|
| CLI tool | Origami transformation, geometric terminal |
| Library | Interconnected building blocks |
| Web app | Modern interface window, minimal chrome |
| API | Messenger bird carrying data packet |
| Framework | Architectural scaffold, blueprint |
| Tool | Precision instrument, sharp edges |
| Converter | Metamorphosis symbol (butterfly) |
| Runner | Sprinter in motion, speed lines |
| Validator | Wax seal of approval |
| Linter | Elegant brush sweeping |
| Test framework | Test tube with checkmarks |
| Dashboard | Mission control panel |
| Analytics | Magnifying glass revealing patterns |
| Database | Stacked cylinders, data nodes |
| Security | Shield, lock, key |
| Default | Abstract geometric shape |

## ❌ DO NOT

- Invent custom visual metaphors (use the table above)
- Paraphrase the template (use it verbatim with values filled in)
- Add extra descriptive language like "network nodes", "data fragments", "circuit patterns", "flowing streams"
- Skip any line of the template
- Add "gradient", "3D", "glossy", "photorealistic" or similar non-minimalist styles
- Include text, letters, or words in the logo description
- Use green tones in the icon colors - green is reserved for the chromakey background
- Infer `--key-color` from background colors in the style text (ALWAYS use `config.keyColor` or default green)

## Configuration Reference

Logo generation can be customized via configuration files. Check in order (first found wins):

1. **Project config**: `./.claude/readme-generator.json`
2. **User config**: `~/.claude/readme-generator.json`
3. **Default config**: `assets/default-config.json` (bundled with this skill)

Read JSON if exists, extract `logo` object. Project overrides user overrides default.

### Configurable Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `iconColors` | `["#58a6ff", "#d29922", "#a371f7", "#7aa2f7", "#f97583"]` | Preferred icon colors (avoid green) |
| `style` | `minimalist` | Logo style description (completely overrides default prompt if set) |
| `size` | `64x64` | Target size for logo |
| `aspectRatio` | `1:1` | Aspect ratio for generation |
| `model` | `google/gemini-3-pro-image-preview` | Model for image generation |
| `keyColor` | `#00FF00` | Chromakey background color (green recommended) |
| `tolerance` | `70` | Chromakey tolerance for transparency (0-255, higher = more aggressive) |

### Example Configuration

**Minimalist style (default):**
```json
{
  "logo": {
    "iconColors": ["#7aa2f7", "#bb9af7", "#7dcfff"],
    "style": "minimalist",
    "model": "google/gemini-3-pro-image-preview",
    "keyColor": "#00FF00",
    "tolerance": 70
  }
}
```

**Pixel art style (SNES/LucasArts aesthetic):**
```json
{
  "logo": {
    "iconColors": "SVGA high-color palette with maximum saturation and vibrancy. Vivid reds, bright oranges, golden yellows, electric cyans, deep blues, bold purples. Avoid green tones.",
    "style": "SNES 16-bit pixel art (Chrono Trigger style). Charming character mascot representing the project concept. VISIBLE CHUNKY PIXELS with dithering for shading. Selective outlines. Full SNES color palette, bright and saturated. Floating icon-only symbols (no text on icons). Banner with project name as pixel art text. Pure bright green (#00FF00) background only - do not use green anywhere else in the design.",
    "keyColor": "#00FF00",
    "tolerance": 70,
    "model": "google/gemini-3-pro-image-preview"
  }
}
```

## Chromakey Transparency

**Workflow:** Gemini generates logo with green (#00FF00) background → PIL converts to transparent with smooth edges.

**Why green?** Industry standard (film/TV green screen). White causes halo artifacts. Magenta conflicts with purple tones in pixel art.

**Flags:**
- `--key-color "#FF00FF"` - Use magenta if design needs green
- `--white-bg` - Legacy white background mode

## PNG Compression

Logos are automatically compressed using **pngquant** (60-80% reduction, preserves alpha quality).

**Install:** `brew install pngquant` (macOS) or `apt install pngquant` (Linux)

**Flags:**
- `--no-compress` - Skip compression
- `--compress-quality 90` - Adjust quality (1-100, default: 80)

If pngquant not installed, compression is skipped with a warning.

## Technical Requirements

Logos must meet these criteria:
- **Centered**: Works in circular and square crops
- **High contrast**: Clear visibility on various backgrounds
- **Clean style**: Works at multiple sizes (16x16 to 512x512)
- **Single focal point**: One clear visual element

## Usage

```bash
# Basic usage (see Path Resolution for $LOGO_SCRIPT)
uv run --with requests --with pillow "$LOGO_SCRIPT" "prompt" --output logo.png

# Optional flags:
#   --keep-original          Save original before transparency
#   --tolerance 80           Chromakey tolerance (default: 70)
#   --key-color "#FF00FF"    Use magenta instead of green
#   --white-bg               Legacy white background mode
#   --no-compress            Skip PNG compression
#   --compress-quality 90    Compression quality (default: 80)
```

**Note:** On macOS, may require `dangerouslyDisableSandbox: true` due to UV accessing system APIs.
