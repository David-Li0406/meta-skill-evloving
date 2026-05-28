# Insert Appendix

Inserts a new appendix BEFORE the specified position, renumbering subsequent appendices.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `position` | Position to insert BEFORE (e.g., "appendix 2", "app02") | Yes |
| `slug` | URL-friendly name | Yes |
| `title` | Display title | Yes |

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Identify appendices to renumber** - All appendices from position onwards
3. **Rename in reverse order** - Highest number first to avoid conflicts
   - Rename folder: `app<NN>-<slug>/` -> `app<NN+1>-<slug>/`
   - Rename appendix file
4. **Load type-specific implementation** - Read `commands/<type>/insert-appendix.md`
5. **Create new appendix** - At the insertion position
6. **Update aggregator** - Update all paths in backmatter aggregator

## Important Notes

- Rename from highest to lowest to avoid file conflicts

## Type-Specific Implementation

Load from: `commands/<type>/insert-appendix.md`
