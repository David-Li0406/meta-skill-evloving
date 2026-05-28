# Rename Appendix

Changes the slug and/or title of an existing appendix.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `current` | Current appendix identifier (number or slug) | Yes |
| `new_slug` | New URL-friendly name (optional) | No |
| `new_title` | New display title (optional) | No |

At least one of `new_slug` or `new_title` must be provided.

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate appendix** - Find appendix by number or slug
3. **Load type-specific implementation** - Read `commands/<type>/rename-appendix.md`
4. **Rename folder and file** - If slug changes
5. **Update appendix content** - Label and title
6. **Update aggregator** - Update path in backmatter aggregator
7. **Update cross-references** - Search project for old label references

## Type-Specific Implementation

Load from: `commands/<type>/rename-appendix.md`
