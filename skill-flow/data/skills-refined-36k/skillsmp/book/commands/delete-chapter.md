# Delete Chapter

Removes a chapter and all its contents.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part containing the chapter | Yes (if ambiguous) |
| `chapter` | Chapter identifier (prefix or slug) | Yes |

## Preconditions

- **Confirm with user** if chapter contains sections or figures

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate chapter** - Find chapter by number or slug
3. **Check contents** - If chapter has content, ask for confirmation
4. **Load type-specific implementation** - Read `commands/<type>/delete-chapter.md`
5. **Delete folder** - Remove entire chapter folder recursively
6. **Update aggregator** - Remove entry from part aggregator

## Important Notes

- Deleting does NOT renumber remaining chapters
- Gaps in numbering are allowed
- Check for broken cross-references after deletion

## Type-Specific Implementation

Load from: `commands/<type>/delete-chapter.md`
