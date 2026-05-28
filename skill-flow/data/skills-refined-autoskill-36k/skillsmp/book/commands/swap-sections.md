# Swap Sections

Exchanges the positions of two sections within a chapter.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Part containing the chapter | Yes (if ambiguous) |
| `chapter` | Chapter containing the sections | Yes |
| `section1` | First section identifier | Yes |
| `section2` | Second section identifier | Yes |

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate both sections** - Find by number or slug
3. **Load type-specific implementation** - Read `commands/<type>/swap-sections.md`
4. **Temporary rename** - Use `.tmp` suffix to avoid conflicts
5. **Swap files** - Exchange numbers
6. **Update labels** - If they include numbers
7. **Update aggregator** - Reorder entries in chapter file

## Workflow Detail

```
sec02-<slug-a>.tex -> sec02-<slug-a>.tex.tmp
sec05-<slug-b>.tex -> sec02-<slug-b>.tex
sec02-<slug-a>.tex.tmp -> sec05-<slug-a>.tex
```

## Type-Specific Implementation

Load from: `commands/<type>/swap-sections.md`
