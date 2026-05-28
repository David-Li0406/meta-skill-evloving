---
name: screenshot-reference
description: Captures and organizes screenshots for fact-checking, source documentation, and progress tracking. Use when asked to take screenshots, document sources, capture progress steps, or create visual references.
---

# Screenshot Reference

Captures screenshots of sources, excerpts, and progress steps, organizing them into subfolders with URL references in documents.

## Directory Structure

```
weeks/YYYY/week-XX/
├── README.md
├── topic-name.md
└── screenshots/
    ├── sources/          # External sources, articles, documentation
    ├── progress/         # Step-by-step progress captures
    └── excerpts/         # Specific quotes or data snippets
```

## Workflow

### 1. Create Screenshot Directory

For each weekly entry with screenshots:

```bash
mkdir -p weeks/YYYY/week-XX/screenshots/{sources,progress,excerpts}
```

### 2. Naming Convention

Use descriptive kebab-case names with date prefix:

- `sources/2025-01-19-article-title.png`
- `progress/step-01-initial-setup.png`
- `excerpts/quote-author-topic.png`

### 3. Reference in Documents

Include screenshots using relative paths:

```markdown
## Sources

![Article screenshot](screenshots/sources/2025-01-19-article-name.png)
*Source: [Article Title](https://example.com/article) - Captured 2025-01-19*

## Progress

| Step | Screenshot | Description |
|------|------------|-------------|
| 1 | ![Step 1](screenshots/progress/step-01-setup.png) | Initial setup |
| 2 | ![Step 2](screenshots/progress/step-02-config.png) | Configuration |
```

### 4. URL Reference Format

Always document the source URL alongside screenshots:

```markdown
> **Fact-check reference:**
> - Screenshot: [view](screenshots/sources/filename.png)
> - Original URL: https://example.com/source
> - Captured: YYYY-MM-DD
```

## Capture Methods

### macOS (built-in)

```bash
# Full screen
screencapture -x screenshots/sources/filename.png

# Selection
screencapture -i screenshots/sources/filename.png

# Window
screencapture -w screenshots/sources/filename.png
```

### Using Chrome DevTools MCP (if available)

```
take_screenshot of the current page
```

## Best Practices

1. **Always include source URL** - Screenshots without context lose value
2. **Use descriptive names** - Future you will thank present you
3. **Date prefix for sources** - Helps track when information was captured
4. **Step numbers for progress** - Maintains order in step-by-step docs
5. **Keep excerpts focused** - Capture only the relevant portion
