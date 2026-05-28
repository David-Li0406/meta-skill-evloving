# Insert Part

Inserts a new part BEFORE the specified position, renumbering subsequent parts.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `position` | Position to insert BEFORE (e.g., "part 2", "part02") | Yes |
| `slug` | URL-friendly name (e.g., "fundamentals") | Yes |
| `title` | Display title (e.g., "Fundamentals") | Yes |

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Identify parts to renumber** - All parts from position onwards
3. **Rename in reverse order** - Highest number first to avoid conflicts
4. **Load type-specific implementation** - Read `commands/<type>/insert-part.md`
5. **Create new part** - At the insertion position
6. **Update aggregator** - Update all paths in bodymatter aggregator

## Important Notes

- Rename from highest to lowest to avoid file conflicts
- Chapter files inside parts do NOT need path updates (they reference `../../main.tex`)

## Type-Specific Implementation

Load from: `commands/<type>/insert-part.md`
