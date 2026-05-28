---
name: md-to-html
description: Convert markdown to styled HTML for pasting into Google Docs. Use when the user wants to copy markdown (with tables, images, code blocks) into Google Docs or similar.
allowed-tools: Bash, Read
---

# Markdown to HTML

Converts markdown files to self-contained, styled HTML optimized for copying into Google Docs. Tables get proper borders, code blocks are styled, and images are embedded.

## Usage

Run the script via bunx:

```bash
bunx ~/nixos-config/modules/programs/claude-code/skills/md-to-html/md-to-html.ts "<markdown-file>"
```

## What it does

1. Converts markdown to HTML via pandoc (uses `nix run` if not installed)
2. Applies clean, modern CSS (system fonts, bordered tables, styled code blocks)
3. Embeds all images as base64 (self-contained)
4. Opens the result in the default browser
5. User can then Cmd+A, Cmd+C, paste into Google Docs

## Output

- Creates `/tmp/<filename>.html`
- Opens in browser automatically

## CSS Features

- System fonts (SF Pro, Segoe UI, etc.)
- Tables: auto-width, 1px borders, grey headers
- Code blocks: light grey background, rounded corners
- Blockquotes: left border accent
- Images: max-width 100%
- Reasonable max-width container (900px)

## Notes

- Requires pandoc (script will use `nix run nixpkgs#pandoc` as fallback)
- Images in markdown must be accessible from the markdown file's directory
- Best results when copying from Safari/Chrome to Google Docs
