---
name: baoyu-multimedia-suite
description: Comprehensive multimedia and social media toolkit. Supports AI image generation, infographics, comics, image compression, and posting to X/WeChat.
---

#  Baoyu Multimedia & Social Suite

This suite contains a collection of specialized tools for visual content creation and distribution.

## ️ Included Tools

### ️ Comic

# Knowledge Comic Creator

Create original knowledge comics with multiple visual styles.

## Usage

```bash
/baoyu-comic posts/turing-story/source.md
/baoyu-comic  # then paste content
```

## Options

| Option | Values |
|--------|--------|
| `--style` | classic (default), dramatic, warm, sepia, vibrant, ohmsha, realistic, wuxia, shoujo, or custom description |
| `--layout` | standard (default), cinematic, dense, splash, mixed, webtoon |
| `--aspect` | 3:4 (default, portrait), 4:3 (landscape), 16:9 (widescreen) |
| `--lang` | auto (default), zh, en, ja, etc. |

> **Full instructions for comic are available in the toolkit.**

### ️ Compress Image

# Image Compressor

Cross-platform image compression with WebP default output, PNG-to-PNG support, preferring system tools with Sharp fallback.

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/main.ts` | CLI entry point for image compression |

## Quick Start

> **Full instructions for compress-image are available in the toolkit.**

### ️ Cover Image

# Cover Image Generator

Generate hand-drawn style cover images for articles with multiple style options.

## Usage

```bash
# From markdown file (auto-select style based on content)
/baoyu-cover-image path/to/article.md

# Specify a style
/baoyu-cover-image path/to/article.md --style blueprint
/baoyu-cover-image path/to/article.md --style warm
/baoyu-cover-image path/to/article.md --style dark-atmospheric

# Without title text
/baoyu-cover-image path/to/article.md --no-title

# Combine options

> **Full instructions for cover-image are available in the toolkit.**

### ️ Image Gen

# Image Generation (AI SDK)

Official API-based image generation via AI SDK. Supports OpenAI (DALL-E, GPT Image) and Google (Imagen, Gemini multimodal).

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/main.ts` | CLI entry point for image generation |

## Quick Start

> **Full instructions for image-gen are available in the toolkit.**

### ️ Infographic

# Infographic Generator

Generate professional infographics with two dimensions: layout (information structure) and style (visual aesthetics).

## Usage

```bash
# Auto-recommend combinations based on content
/baoyu-infographic path/to/content.md

# Specify layout
/baoyu-infographic path/to/content.md --layout hierarchical-layers

# Specify style (default: craft-handmade)
/baoyu-infographic path/to/content.md --style technical-schematic

# Specify both
/baoyu-infographic path/to/content.md --layout funnel --style corporate-memphis


> **Full instructions for infographic are available in the toolkit.**

### ️ Xhs Images

# Xiaohongshu Infographic Series Generator

Break down complex content into eye-catching infographic series for Xiaohongshu with multiple style options.

## Usage

```bash
# Auto-select style and layout based on content
/baoyu-xhs-images posts/ai-future/article.md

# Specify style
/baoyu-xhs-images posts/ai-future/article.md --style notion

# Specify layout
/baoyu-xhs-images posts/ai-future/article.md --layout dense

# Combine style and layout
/baoyu-xhs-images posts/ai-future/article.md --style notion --layout list


> **Full instructions for xhs-images are available in the toolkit.**

### ️ Article Illustrator

# Smart Article Illustration Skill

Analyze article structure and content, identify positions requiring visual aids, and generate illustrations with flexible style options.

## Usage

```bash
# Auto-select style based on content
/baoyu-article-illustrator path/to/article.md

# Specify a style
/baoyu-article-illustrator path/to/article.md --style warm
/baoyu-article-illustrator path/to/article.md --style minimal
/baoyu-article-illustrator path/to/article.md --style watercolor

# Combine with other options
/baoyu-article-illustrator path/to/article.md --style playful
```


> **Full instructions for article-illustrator are available in the toolkit.**

### ️ Danger Gemini Web

# Gemini Web Client

Supports:
- Text generation
- Image generation (download + save)
- Reference images for vision input (attach local images)
- Multi-turn conversations via persisted `--sessionId`

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |

> **Full instructions for danger-gemini-web are available in the toolkit.**

### ️ Post To Wechat

# Post to WeChat Official Account (微信公众号)

Post content to WeChat Official Account using Chrome CDP automation.

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/wechat-browser.ts` | Image-text posts (图文) |
| `scripts/wechat-article.ts` | Full article posting (文章) |
| `scripts/md-to-wechat.ts` | Markdown → WeChat HTML conversion |

> **Full instructions for post-to-wechat are available in the toolkit.**

### ️ Post To X

# Post to X (Twitter)

Post content, images, videos, and long-form articles to X using real Chrome browser (bypasses anti-bot detection).

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

**Script Reference**:
| Script | Purpose |
|--------|---------|
| `scripts/x-browser.ts` | Regular posts (text + images) |
| `scripts/x-video.ts` | Video posts (text + video) |
| `scripts/x-quote.ts` | Quote tweet with comment |

> **Full instructions for post-to-x are available in the toolkit.**

### ️ Slide Deck

# Slide Deck Generator

Transform content into professional slide deck images with flexible style options.

## Usage

```bash
/baoyu-slide-deck path/to/content.md
/baoyu-slide-deck path/to/content.md --style sketch-notes
/baoyu-slide-deck path/to/content.md --audience executives
/baoyu-slide-deck path/to/content.md --lang zh
/baoyu-slide-deck path/to/content.md --slides 10
/baoyu-slide-deck path/to/content.md --outline-only
/baoyu-slide-deck  # Then paste content
```

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

> **Full instructions for slide-deck are available in the toolkit.**
