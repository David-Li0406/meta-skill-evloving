# New Appendix

Appends a new appendix at the end of backmatter.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `slug` | URL-friendly name (e.g., "formulas") | Yes |
| `title` | Display title (e.g., "Mathematical Formulas") | Yes |

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Find existing appendices** - Count appendices in `<type>/300-backmatter/`
3. **Calculate next number** - Use next available appendix number (app01, app02, etc.)
4. **Load type-specific implementation** - Read `commands/<type>/new-appendix.md`
5. **Create files** - Appendix folder and file
6. **Update aggregator** - Add entry to backmatter aggregator

## Type-Specific Implementation

Load from: `commands/<type>/new-appendix.md`
