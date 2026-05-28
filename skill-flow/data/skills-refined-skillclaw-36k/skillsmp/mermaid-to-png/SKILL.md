---
name: mermaid-to-png
description: Convert mermaid diagrams in markdown files to PNG images. Use when the user wants to export markdown with mermaid to formats that don't support mermaid (Google Docs, PDF, etc).
allowed-tools: Bash, Read
---

# Mermaid to PNG

Extracts mermaid diagrams from markdown files, renders them to PNGs, and inserts image references after each mermaid block. The original mermaid code is preserved for future editing.

## Usage

Run the script via bunx:

```bash
bunx ~/nixos-config/modules/programs/claude-code/skills/mermaid-to-png/mermaid-to-png.ts "<markdown-file>"
```

## What it does

1. Finds all ```` ```mermaid ```` code blocks in the markdown file
2. Renders each to PNG via mermaid.ink API (no local browser needed)
3. Saves PNGs to `assets/<filename-kebab-case>/diagram-N.png`
4. Inserts `![Diagram N](assets/...)` after each mermaid block
5. Preserves original mermaid code for future edits

## Output structure

```
document.md
assets/
  document/
    diagram-1.png
    diagram-2.png
    ...
```

## Example

**Before:**
````markdown
# My Doc

```mermaid
graph LR
    A --> B
```
````

**After:**
````markdown
# My Doc

```mermaid
graph LR
    A --> B
```

![Diagram 1](assets/my-doc/diagram-1.png)
````

## Notes

- Uses mermaid.ink web API (requires internet)
- Filenames are converted to kebab-case (no spaces)
- White background for compatibility
- Idempotent: re-running will regenerate PNGs but not duplicate image refs (mermaid blocks without existing image refs get new ones)
