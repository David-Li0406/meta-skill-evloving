# Insert Section

Inserts a new section BEFORE the specified position, renumbering subsequent sections.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part containing the chapter | Yes (if ambiguous) |
| `chapter` | Chapter containing the sections | Yes |
| `position` | Position to insert BEFORE (e.g., "section 3", "sec03") | Yes |
| `slug` | URL-friendly name | Yes |
| `title` | Display title | Yes |

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate chapter and section position** - Validate position exists
3. **Identify sections to renumber** - All sections from position onwards
4. **Rename in reverse order** - Highest number first to avoid conflicts
   - Rename file: `sec<NN>-<slug>.tex` -> `sec<NN+1>-<slug>.tex`
5. **Load type-specific implementation** - Read `commands/<type>/insert-section.md`
6. **Create new section** - At the insertion position
7. **Update aggregator** - Update all paths in chapter file

## Important Notes

- Rename from highest to lowest to avoid file conflicts
- Labels using slugs (not numbers) do NOT need updating

## Type-Specific Implementation

Load from: `commands/<type>/insert-section.md`
