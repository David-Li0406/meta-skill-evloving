# Delete Section

Removes a section file.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part containing the chapter | Yes (if ambiguous) |
| `chapter` | Chapter containing the section | Yes |
| `section` | Section identifier (prefix or slug) | Yes |

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate section** - Find section by number or slug
3. **Load type-specific implementation** - Read `commands/<type>/delete-section.md`
4. **Delete file** - Remove section file
5. **Update aggregator** - Remove entry from chapter file

## Important Notes

- Deleting does NOT renumber remaining sections
- Gaps in numbering are allowed
- Check for broken cross-references after deletion

## Type-Specific Implementation

Load from: `commands/<type>/delete-section.md`
