# Move Section

Moves a section from one chapter to another.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `source_part` | Part containing source chapter | Yes (if ambiguous) |
| `source_chapter` | Chapter containing the section | Yes |
| `section` | Section to move | Yes |
| `target_part` | Part containing target chapter | Yes (if ambiguous) |
| `target_chapter` | Destination chapter | Yes |

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate source section** - Find section in source chapter
3. **Determine target number** - Next available section number in target chapter
4. **Load type-specific implementation** - Read `commands/<type>/move-section.md`
5. **Move file** - To target chapter with new number
6. **Update section content** - Update label to reference new chapter
7. **Update source aggregator** - Remove entry from source chapter
8. **Update target aggregator** - Add entry to target chapter

## Important Notes

- Labels typically include chapter reference: `sec:<chapter>:<slug>`
- Update label to reference new chapter

## Type-Specific Implementation

Load from: `commands/<type>/move-section.md`
