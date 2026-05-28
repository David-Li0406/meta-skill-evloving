# New Section

Appends a new section at the end of a chapter.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part containing the chapter | Yes (if ambiguous) |
| `chapter` | Target chapter | Yes |
| `slug` | URL-friendly name (e.g., "methodology") | Yes |
| `title` | Display title (e.g., "Methodology") | Yes |

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate chapter** - Find target chapter folder
3. **Find existing sections** - Count sections in chapter
4. **Calculate next number** - Use next available section number (sec01, sec02, etc.)
5. **Load type-specific implementation** - Read `commands/<type>/new-section.md`
6. **Create file** - Section file in chapter folder
7. **Update aggregator** - Add entry to chapter file

## Type-Specific Implementation

Load from: `commands/<type>/new-section.md`
