# Move Chapter

Moves a chapter from one part to another.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `source_part` | Part containing the chapter | Yes |
| `chapter` | Chapter to move | Yes |
| `target_part` | Destination part | Yes |
| `position` | Position in target (optional, defaults to end) | No |

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate source chapter** - Find chapter in source part
3. **Determine target number** - Next available or specified position
4. **Handle numbering scheme change** - Roman to arabic or vice versa if crossing part types
5. **Load type-specific implementation** - Read `commands/<type>/move-chapter.md`
6. **Move folder** - To target part with new number
7. **Rename files** - If numbering scheme changes
8. **Update source aggregator** - Remove entry
9. **Update target aggregator** - Add entry

## Important Notes

- If moving from part01 (roman) to part02 (arabic), numbering scheme changes
- Update labels if they include the part reference

## Type-Specific Implementation

Load from: `commands/<type>/move-chapter.md`
