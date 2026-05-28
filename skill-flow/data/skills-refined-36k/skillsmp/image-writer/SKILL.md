---
name: image-writer
description: Create new "image" entries - visual content with brief captions. Use when the user says "add an image", "new image", "post an image", or mentions wanting to share a screenshot, photo, or visualization.
allowed-tools:
  - Write
  - Read
  - Bash
---

# Image Writer

This skill creates new "image" entries - visual content with brief captions that appear in the homepage feed alongside your thoughts, ideas, and articles.

## File Locations

- **Content files**: `src/content/images/`
- **Physical images**: `/public/images/`

**IMPORTANT**: You must place the physical image file in `/public/images/` before creating the content entry.

## Filename Format

Use the format `YYMMDD.md` where:
- `YY` = 2-digit year (e.g., `25` for 2025)
- `MM` = 2-digit month (e.g., `01`, `12`)
- `DD` = 2-digit day (e.g., `05`, `31`)

Example: `260114.md` for January 14, 2026

## Image File Naming

For the physical image in `/public/images/`, use descriptive names like:
- `YYMMDD_description.ext` (e.g., `260114_dashboard.png`)
- `YYMMDD_screenshot.ext` (e.g., `260114_terminal.png`)
- `YYMMDD_photo.ext` (e.g., `260114_conference.jpg`)

This keeps things organized and makes images easy to find.

## Frontmatter Schema

```yaml
---
date: YYYY-MM-DD              # required
imageUrl: /images/filename.ext  # required (path from /public/images/)
draft: false                   # optional, defaults to false
author: Nikola Balić           # optional, defaults to Nikola Balić
---
```

**Field details:**
- `date`: Required, YYYY-MM-DD format.
- `imageUrl`: Required, path to image in `/public/images/`. Must start with `/images/`.
- `draft`: Optional, defaults to false.
- `author`: Optional, defaults to "Nikola Balić".

## Content Style Guidelines

Image captions should be brief and contextual:

- **Length**: 1-2 sentences typical (can be longer if needed)
- **Purpose**: Contextualize what the image shows
- **Style**: Conversational, can include links and emojis
- **Content**: Explain the "why" behind the image, not just "what" it is

## Examples

**Social media mention:**
```markdown
---
date: 2025-05-19
imageUrl: /images/250523_oreillyandkentbeck.jpeg
---

Apparently, @timoreilly considered it [noteworthy to highlight](https://www.oreilly.com/radar/takeaways-from-coding-with-ai/) that I agree with @KentBeck 🤷‍♂️ honored and humbled!
```

**Dashboard visualization:**
```markdown
---
date: 2025-05-26
imageUrl: /images/apnea-comprehensive_dashboard.png
---

Claude 4 Sonnet loves complex dashboard visualisations. I have been playing with my Garmin data to better understand agentic future of data science research.
```

**Screenshot/photo with context:**
```markdown
---
date: 2025-05-23
imageUrl: /images/250523_claude4imagecritic.jpeg
---

Claude 4 as image critic.
```

## When to Use Images vs Other Content Types

| Type | When to use | Format |
|------|-------------|--------|
| **Image** | Visual content (screenshot, photo, chart) with brief caption | date + imageUrl, YYMMDD.md |
| **Thought** | Quick insight, observation, philosophical reflection | Minimal frontmatter, blockquote style |
| **Idea** | Product/service concept with marketing flair | Structured frontmatter, pitch style |
| **Now Entry** | Life update with multiple focus areas | YYMMDD.md, ## sections |
| **Article** | Full blog post with narrative/technical depth | Complete frontmatter (tags, topics, etc.) |

## How It Works

- Images appear on the homepage (`/`) in the main feed
- Integrated with search at `/search`
- Displayed with image and caption together
- Sorted chronologically (newest first)

## Process

When the user wants to add an image:

1. **Confirm the image file exists** in `/public/images/`
2. **Get the image filename** for the `imageUrl` field
3. **Determine today's date** for the filename (YYMMDD.md) and frontmatter (YYYY-MM-DD)
4. **Ask what context/caption** they want to add
5. **Draft the caption** following the style guidelines
6. **Create the file** in `src/content/images/`
7. **Confirm creation** with the user

## Important Reminders

- **Always** verify the physical image exists in `/public/images/` first
- The `imageUrl` must start with `/images/` (not `/public/images/`)
- Image files can be any format: `.jpg`, `.png`, `.jpeg`, `.gif`, `.webp`, etc.
- Keep captions brief - this isn't a blog article, just context for the visual
