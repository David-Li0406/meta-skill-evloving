# Swap Chapters

Exchanges the positions of two chapters.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part containing the chapters | Yes (if ambiguous) |
| `chapter1` | First chapter identifier | Yes |
| `chapter2` | Second chapter identifier | Yes |

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate both chapters** - Find by number or slug
3. **Load type-specific implementation** - Read `commands/<type>/swap-chapters.md`
4. **Temporary rename** - Use `.tmp` suffix to avoid conflicts
5. **Swap folders and files** - Exchange numbers
6. **Update labels** - If they include numbers
7. **Update aggregator** - Reorder entries in part aggregator

## Workflow Detail

```
ch02-<slug-a>/ -> ch02-<slug-a>.tmp/
ch05-<slug-b>/ -> ch02-<slug-b>/
ch02-<slug-a>.tmp/ -> ch05-<slug-a>/
```

## Type-Specific Implementation

Load from: `commands/<type>/swap-chapters.md`
