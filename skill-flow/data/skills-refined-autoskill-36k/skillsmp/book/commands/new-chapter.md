# New Chapter

Appends a new chapter at the end of a part.

## Required Information

| Field | Description | Ask if missing |
|-------|-------------|----------------|
| `part` | Target part (e.g., "part02", "part 2") | Yes |
| `slug` | URL-friendly name (e.g., "transport-optimization") | Yes |
| `title` | Display title (e.g., "Transport Optimization") | Yes |

## Workflow

1. **Read config** - Determine active filetype from `<type>/config.yaml`
2. **Locate part** - Find target part folder
3. **Find existing chapters** - Count chapters in part
4. **Determine numbering scheme** - Part01 uses roman (chi, chii), Part02+ uses arabic (ch01, ch02)
5. **Calculate next number** - Use next available chapter number
6. **Load type-specific implementation** - Read `commands/<type>/new-chapter.md`
7. **Create files** - Chapter folder, chapter file, figures folder
8. **Update aggregator** - Add entry to part aggregator

## Numbering Schemes

| Part | Prefix Pattern | Examples |
|------|---------------|----------|
| part01 | `ch<roman>` | chi, chii, chiii |
| part02+ | `ch<NN>` | ch01, ch02, ch10 |

## Type-Specific Implementation

Load from: `commands/<type>/new-chapter.md`
