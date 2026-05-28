# Delete Appendix

Removes an appendix and all its contents.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `appendix` | Appendix identifier (number or slug) | Yes |

## Preconditions

- **Confirm with user** if appendix has content

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate appendix** - Find appendix by number or slug
3. **Check contents** - If appendix has content, ask for confirmation
4. **Load type-specific implementation** - Read `commands/<type>/delete-appendix.md`
5. **Delete folder** - Remove entire appendix folder recursively
6. **Update aggregator** - Remove entry from backmatter aggregator

## Important Notes

- Deleting does NOT renumber remaining appendices
- Gaps in numbering are allowed
- Check for broken cross-references after deletion

## Type-Specific Implementation

Load from: `commands/<type>/delete-appendix.md`
