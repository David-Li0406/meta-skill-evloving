# New Part

Appends a new part at the end of bodymatter.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `slug` | URL-friendly name (e.g., "advanced-topics") | Yes |
| `title` | Display title (e.g., "Advanced Topics") | Yes |

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Find existing parts** - Count parts in `<type>/200-bodymatter/`
3. **Calculate next number** - Use next available part number (01, 02, etc.)
4. **Load type-specific implementation** - Read `commands/<type>/new-part.md`
5. **Create files** - Follow type-specific file creation
6. **Update aggregator** - Add entry to bodymatter aggregator

## Type-Specific Implementation

Load from: `commands/<type>/new-part.md`
