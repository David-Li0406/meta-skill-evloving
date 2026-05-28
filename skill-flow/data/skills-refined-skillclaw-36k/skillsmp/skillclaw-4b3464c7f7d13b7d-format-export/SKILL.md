---
name: format-export
description: Use this skill when you need to export a screenplay to PDF, convert it to Final Draft (FDX), generate an HTML preview, or prepare scripts for delivery.
---

# Format Export Skill

## Invocation Triggers
Apply this skill when:
- Exporting screenplay to PDF
- Converting to Final Draft (FDX)
- Generating HTML preview
- Preparing scripts for delivery

## Recommended: Better Fountain Extension

The simplest export method uses the [Better Fountain](https://marketplace.visualstudio.com/items?itemName=piersdeseilligny.betterfountain) VS Code extension:

| Format | Command Palette Action |
|--------|------------------------|
| PDF | `Fountain: Export to PDF` |
| FDX | `Fountain: Export to FDX` |
| HTML | `Fountain: Export to HTML` |

**Steps:**
1. Open your `.fountain` file in VS Code.
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS).
3. Type the export command.
4. Choose the output location.

## Export Formats Overview

| Format | Extension | Purpose | Tools |
|--------|-----------|---------|-------|
| PDF | .pdf | Industry standard delivery | Better Fountain, afterwriting, Highland |
| FDX | .fdx | Final Draft import | Better Fountain, screenplain, Highland |
| HTML | .html | Web preview/sharing | Better Fountain, afterwriting |
| Plain Text | .txt | Accessibility, archival | direct copy |

## PDF Export

### Industry Standard Format
- **Font:** Courier 12pt
- **Margins:** 1.5" left, 1" right, 1" top/bottom
- **Page Size:** US Letter (8.5" x 11")
- **Page Numbers:** Top right, starting from page 2

### Better Fountain (Recommended)
In VS Code: `Ctrl+Shift+P` → "Fountain: Export to PDF"

### CLI: afterwriting (for automation)
```bash
# Install
npm install -g afterwriting

# Basic PDF export
afterwriting --source screenplay.fountain --pdf

# With configuration
afterwriting --source screenplay.fountain --pdf --config pdf-config.json

# Output to specific file
afterwriting --source screenplay.fountain --pdf --output script.pdf
```

### PDF Configuration (pdf-config.json)
```json
{
  "print_title_page": true,
  "print_profile": "default",
  "print_header": "",
  "print_footer": "",
  "print_watermark": "",
  "print_dialogue_numbers": false,
  "print_notes": false,
  "print_sections": false,
  "print_synopses": false,
  "scenes_numbers": "non"
}
```