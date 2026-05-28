# Rename Section

Changes the slug and/or title of an existing section.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part containing the chapter | Yes (if ambiguous) |
| `chapter` | Chapter containing the section | Yes |
| `current` | Current section identifier (prefix or slug) | Yes |
| `new_slug` | New URL-friendly name (optional) | No |
| `new_title` | New display title (optional) | No |

At least one of `new_slug` or `new_title` must be provided.

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate section** - Find section by number or slug
3. **Load type-specific implementation** - Read `commands/<type>/rename-section.md`
4. **Rename file** - If slug changes
5. **Update section content** - Label and title
6. **Update aggregator** - Update path in chapter file
7. **Update cross-references** - Search project for old label references

## Type-Specific Implementation

Load from: `commands/<type>/rename-section.md`
