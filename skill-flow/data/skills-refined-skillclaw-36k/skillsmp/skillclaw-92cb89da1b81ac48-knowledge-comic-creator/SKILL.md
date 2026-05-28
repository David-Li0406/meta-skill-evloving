---
name: knowledge-comic-creator
description: Use this skill when you want to create original educational comics with various art styles and tones, suitable for topics like "知识漫画", "教育漫画", "biography comic", or "tutorial comic".
---

# Knowledge Comic Creator

Create original knowledge comics with flexible art style and tone combinations.

## Usage

```bash
/knowledge-comic-creator posts/turing-story/source.md
/knowledge-comic-creator article.md --style manga --tone warm
/knowledge-comic-creator  # then paste content
```

## Options

### Visual Styles

| Option | Values | Description |
|--------|--------|-------------|
| `--style` | classic (default), dramatic, warm, sepia, vibrant, ohmsha, realistic, wuxia, shoujo, manga, ligne-claire | Art style / rendering technique |
| `--layout` | standard (default), cinematic, dense, splash, mixed, webtoon | Panel arrangement |
| `--aspect` | 3:4 (default, portrait), 4:3 (landscape), 16:9 (widescreen) | Page aspect ratio |
| `--lang` | auto (default), zh, en, ja, etc. | Output language |

### Tones

| Tone | Description |
|------|-------------|
| `neutral` | Balanced, rational, educational |
| `warm` | Nostalgic, personal, comforting |
| `dramatic` | High contrast, intense, powerful |
| `romantic` | Soft, beautiful, decorative elements |
| `energetic` | Bright, dynamic, exciting |
| `vintage` | Historical, aged, period authenticity |
| `action` | Speed lines, impact effects, combat |

### Auto Selection

| Content Signals | Style | Layout |
|-----------------|-------|--------|
| Tutorial, how-to, beginner | ohmsha | webtoon |
| Computing, AI, programming | ohmsha | dense |
| Pre-1950, classical, ancient | sepia | cinematic |
| Personal story, mentor | warm | standard |
| Conflict, breakthrough | dramatic | splash |
| Wine, food, business, lifestyle, professional | realistic | cinematic |
| Martial arts, wuxia, xianxia, Chinese historical | wuxia | splash |
| Romance, love, school life, friendship, emotional | shoujo | standard |
| Biography, balanced | classic | mixed |

## Preset Shortcuts

Presets with special rules beyond style and tone:

| Preset | Equivalent | Special Rules |
|--------|-----------|---------------|
| `--style ohmsha` | `--style manga --tone neutral` | Visual metaphors, NO talking heads, gadget reveals |
| `--style wuxia` | `--style ink-brush --tone action` | Qi effects, combat visuals, atmospheric elements |
| `--style shoujo` | `--style manga --tone romantic` | Decorative elements, eye details, romantic themes |

## File Structure

Each session creates an independent directory named by content slug:

```
comic/{topic-slug}/
├── source-{slug}.{ext}            # Source files (text, images, etc.)
├── analysis.md                    # Deep analysis results (YAML+MD)
├── storyboard-chronological.md    # Variant A (preserved)
├── storyboard-thematic.md         # Variant B (preserved)
├── storyboard-character.md         # Variant C (preserved)
```