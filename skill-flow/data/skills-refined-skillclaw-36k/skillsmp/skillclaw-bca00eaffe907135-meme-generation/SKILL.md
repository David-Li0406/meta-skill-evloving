---
name: meme-generation
description: Use this skill when users request memes, want to add humor to content, or need visual aids for social media. It supports 100+ popular meme templates with custom text and styling options.
---

# Meme Generation with Memegen.link

This skill enables the creation of memes using the free and open-source memegen.link API.

## Quick Reference

**For comprehensive meme creation guidance:**
- See [Complete Markdown Memes Guide](complete-markdown-memes-guide.md) for **15+ textual meme formats** (greentext, copypasta, ASCII art, chat logs, Reddit AITA, Tumblr chains, wojak dialogues, etc.) AND image meme techniques.

## Overview

The memegen.link API allows you to:
- Generate memes using 100+ popular templates.
- Add custom top and bottom text.
- Use custom images as backgrounds.
- Control dimensions, fonts, and styles.
- Create animated memes with GIF/WebP support.

## Quick Start

### Basic Meme Structure

**URL Format:**
```
https://api.memegen.link/images/{template}/{top_text}/{bottom_text}.{extension}
```

**Example:**
```
https://api.memegen.link/images/buzz/memes/memes_everywhere.png
```
This generates a Buzz Lightyear meme with "memes" at the top and "memes everywhere" at the bottom.

### Text Formatting

- **Spacing:** Use **underscores** (`_`) or **dashes** (`-`) for spaces in text.
  - Example: `One_Does_Not_Simply` → "One Does Not Simply"
- **Special Characters:** Use URL encoding for special characters:
  - Spaces: `_` or `-`
  - Newlines: `~n`
  - Question mark: `~q`
  - Percent: `~p`
  - Slash: `~s`
  - Hash/Pound: `~h`
  - Quotes: `''` for single, `""` for double

### Available Templates

**Popular Templates:**
- `buzz` - Buzz Lightyear ("X, X Everywhere")
- `drake` - Drake Hotline Bling (two panels)
- `doge` - Doge (multiple text positions)
- `distracted` - Distracted Boyfriend
- `changemind` - Change My Mind
- `success` - Success Kid
- `skeptical` - Skeptical Third World Kid
- `awesome` - Awesome/Awkward Penguin
- `yodawg` - Yo Dawg
- `ancient` - Ancient Aliens Guy
- `wonka` - Condescending Wonka

**View all templates:**
- API endpoint: `https://api.memegen.link/templates/`
- Interactive docs: `https://api.memegen.link/docs/`

## Advanced Features

- **Custom Backgrounds:** Use the `?style=` parameter to specify a custom image URL.
- **Sizing Options:** Adjust the meme dimensions with `?width=` and `?height=` parameters.

This skill provides a comprehensive approach to meme generation, ensuring users can create engaging and humorous content easily.