# Rename Chapter

Changes the slug and/or title of an existing chapter.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part containing the chapter | Yes (if ambiguous) |
| `current` | Current chapter identifier (prefix or slug) | Yes |
| `new_slug` | New URL-friendly name (optional) | No |
| `new_title` | New display title (optional) | No |

At least one of `new_slug` or `new_title` must be provided.

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate chapter** - Find chapter by number or slug
3. **Load type-specific implementation** - Read `commands/<type>/rename-chapter.md`
4. **Rename folder and file** - If slug changes
5. **Update chapter content** - Label and title
6. **Update aggregator** - Update path in part aggregator
7. **Update cross-references** - Search project for old label references

## Important Notes

- Section files do NOT need path updates
- Search entire project for `\ref{ch:<old-slug>}` and update

## Type-Specific Implementation

Load from: `commands/<type>/rename-chapter.md`
