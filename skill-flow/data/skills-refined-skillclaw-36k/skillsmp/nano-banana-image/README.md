# nano-banana-image

A Claude Code skill for generating images using Google's Gemini API.

## Install

```bash
npx add-skill byrencheema/nano-banana-image
```

Or manually:

```bash
git clone https://github.com/byrencheema/nano-banana-image.git
cd nano-banana-image
./install.sh
```

Then add your API key to your shell config:

```bash
echo 'export GEMINI_API_KEY="your-key"' >> ~/.zshrc
```

Get a key at [Google AI Studio](https://aistudio.google.com/apikey).

## Usage

Once installed, just ask Claude Code to generate images:

> "Generate a logo for my app"
> "Create a 16:9 abstract background"
> "Edit this image to make it more colorful"

## Manual Usage

```bash
cd ~/.claude/skills/nano-banana-image

node scripts/nano_banana.js \
  --model flash \
  --prompt "A minimalist logo" \
  --out output.png
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--model` | `flash` (fast) or `pro` (high quality) | `flash` |
| `--prompt` | Image description | required |
| `--input` | Input image for editing | none |
| `--out` | Output path | `outputs/output.png` |
| `--aspect` | `1:1`, `16:9`, `9:16`, `4:3`, `3:4` | `1:1` |

### Models

| Model | API Name | Features |
|-------|----------|----------|
| `flash` | `gemini-2.5-flash-image` | Fast, supports editing |
| `pro` | `imagen-4.0-generate-001` | Higher quality |

## Rate Limits

Free tier: ~2-3 images/day (resets midnight PT)
