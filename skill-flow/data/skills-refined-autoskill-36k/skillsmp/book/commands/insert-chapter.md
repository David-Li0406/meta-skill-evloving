# Insert Chapter

Inserts a new chapter BEFORE the specified position, renumbering subsequent chapters.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Target part | Yes |
| `position` | Position to insert BEFORE (e.g., "chapter 2", "ch02", "chii") | Yes |
| `slug` | URL-friendly name | Yes |
| `title` | Display title | Yes |

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate part and chapter position** - Validate position exists
3. **Identify chapters to renumber** - All chapters from position onwards
4. **Rename in reverse order** - Highest number first to avoid conflicts
   - Rename folder: `ch<XX>-<slug>/` -> `ch<XX+1>-<slug>/`
   - Rename chapter file
   - Update section files if needed
5. **Load type-specific implementation** - Read `commands/<type>/insert-chapter.md`
6. **Create new chapter** - At the insertion position
7. **Update aggregator** - Update all paths in part aggregator

## Important Notes

- Rename from highest to lowest to avoid file conflicts
- Labels using slugs (not numbers) do NOT need updating
- Cross-references using numeric labels may need updating

## Type-Specific Implementation

Load from: `commands/<type>/insert-chapter.md`
