# Gemini Image Generator

AI image generation using Google Gemini for game assets.

## Expertise

This skill provides:

- **Text-to-Image Generation**: Create images from text prompts
- **Style Transfer**: Use reference images to maintain art consistency
- **Prompt Engineering**: Optimized prompts for game assets
- **Asset Pipeline Integration**: Works with Recraft for full pipeline

## When to Use

Invoke this skill when you need to:

- Generate concept art
- Create game sprites and characters
- Design UI elements
- Produce promotional images
- Explore visual directions quickly

## Setup

### 1. Get API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Create or sign in to your Google account
3. Generate an API key

### 2. Set Environment Variable

```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Install Dependencies

```bash
cd scripts
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Usage

### Basic Generation

```bash
python scripts/generate.py \
  --prompt "A cute robot with brass gears, cartoon style" \
  --output robot.png
```

### With Style Reference

```bash
python scripts/generate.py \
  --prompt "A friendly bee character in the same art style" \
  --reference style-guide.png \
  --output bee.png
```

## Prompt Engineering

### Structure

```
[Subject] + [Style] + [Composition] + [Technical] + [Mood]
```

### Game Asset Prompts

**Character Sprite:**
```
"A cute whimsical robot companion with Art Nouveau brass gears
and botanical vine patterns, soft stylized 3D cartoon rendering,
centered composition, transparent background, warm golden hour
lighting, charming and friendly"
```

**UI Icon:**
```
"Golden coin with leaf emblem, flat vector style, clean simple
design, game UI icon, solid color background, crisp edges"
```

**Background:**
```
"Rolling farmland hills at sunset, soft painterly style, wide
panoramic view, warm orange and purple sky, cozy pastoral mood"
```

### Style Keywords

| Category | Keywords |
|----------|----------|
| Art Style | Art Nouveau, cartoon, vector, pixel art, watercolor |
| Mood | Whimsical, cozy, charming, dramatic, ethereal |
| Technical | Transparent background, centered, game sprite |
| Lighting | Golden hour, soft shadows, warm tones |

## Pipeline Integration

This generator is step 1 in the full asset pipeline:

```
Gemini Generate → Recraft Remove BG → Recraft Vectorize
     ↓                    ↓                   ↓
  concept.png      sprite-nobg.png       sprite.svg
```

## Output Specifications

| Setting | Value |
|---------|-------|
| Model | gemini-2.0-flash-exp |
| Output Format | PNG |
| Typical Size | 1-2 MB |
| Resolution | ~1024x1024 |

## Best Practices

### For Consistent Style
- Always use a reference image for character work
- Keep a "style guide" image for the project
- Include style keywords in every prompt

### For Game Assets
- Request "transparent background" for sprites
- Use "centered composition" for icons
- Specify "game sprite" or "UI element"

### For Quality
- Be specific about details you want
- Include mood/lighting descriptors
- Iterate with refined prompts

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API key invalid | Check GEMINI_API_KEY is set |
| No image generated | Simplify prompt, check quota |
| Wrong style | Use reference image |
| Low quality | Add detail to prompt |

## Integration

This skill works alongside:

- `game-assets-team` - Art direction and briefs
- Recraft API - Background removal and vectorization
- `react-game-ui` - Implementing generated assets

## Usage in Claude Code

```
/gemini-image-generator

"Generate a Simulin robot character..."
"Create an icon for the inventory..."
"Make a background for the farm scene..."
```
