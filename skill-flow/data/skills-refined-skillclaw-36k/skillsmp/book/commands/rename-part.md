# Rename Part

Changes the slug and/or title of an existing part.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `current` | Current part identifier (number or slug) | Yes |
| `new_slug` | New URL-friendly name (optional) | No |
| `new_title` | New display title (optional) | No |

At least one of `new_slug` or `new_title` must be provided.

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate part** - Find part by number or slug
3. **Load type-specific implementation** - Read `commands/<type>/rename-part.md`
4. **Rename folder** - If slug changes
5. **Update aggregator** - Update paths and title in bodymatter aggregator

## Important Notes

- Child chapter files do NOT need updating (they reference relative paths to main)
- Only the folder name and aggregator references change

## Type-Specific Implementation

Load from: `commands/<type>/rename-part.md`
