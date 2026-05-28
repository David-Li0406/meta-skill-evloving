# Delete Part

Removes a part and all its contents.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part identifier (number or slug) | Yes |

## Preconditions

- **Confirm with user** if part contains chapters

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate part** - Find part by number or slug
3. **Check contents** - If part has chapters, ask for confirmation
4. **Load type-specific implementation** - Read `commands/<type>/delete-part.md`
5. **Delete folder** - Remove entire part folder recursively
6. **Update aggregator** - Remove entry from bodymatter aggregator

## Important Notes

- Deleting does NOT renumber remaining parts
- Gaps in numbering are allowed

## Type-Specific Implementation

Load from: `commands/<type>/delete-part.md`
