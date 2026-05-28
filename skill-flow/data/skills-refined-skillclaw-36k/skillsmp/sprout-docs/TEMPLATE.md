# README Template Reference

This template defines the structure that `sprout-docs` generates and validates against.

## Standard Template

```markdown
[← parent](../README.md) · **folder-name**

# Folder Name

> Purpose: Brief explanation of WHY this folder exists.

## Contents

| Item | Purpose |
|------|---------|
| [`example.ts`](./example.ts) | What this file does |
| [`subfolder/`](./subfolder/) | What this subfolder contains |

## Relationships

- **Used by**: Links to consumers
- **Depends on**: Links to dependencies

---
*[View on main](../../tree/main/path/to/folder) · Updated: YYYY-MM-DD*
```

## Template Variants

### Root README (/)

```markdown
# Project Name

> One-line project description

## Quick Links

| Directory | Purpose |
|-----------|---------|
| [`src/`](./src/) | Source code |
| [`docs/`](./docs/) | Documentation |
| [`tests/`](./tests/) | Test suites |

## Getting Started

[Link to main docs or setup instructions]

---
*Auto-generated documentation · [View source](../../tree/main)*
```

### Leaf Folder (no subfolders)

```markdown
[← parent](../README.md) · **utils**

# Utils

> Shared utility functions used across the application.

## Contents

| File | Purpose |
|------|---------|
| [`format.ts`](./format.ts) | Date and string formatting |
| [`validate.ts`](./validate.ts) | Input validation helpers |
| [`index.ts`](./index.ts) | Public exports |

## Relationships

- **Used by**: Most components in `../components/`
- **Standalone**: No external dependencies

---
*Updated: 2024-01-06*
```

### Deep Folder (depth > 2)

```markdown
[← parent](../README.md) · **Button** · [root](/README.md)

# Button Component

> Primary interactive button with multiple variants.

## Contents

| File | Purpose |
|------|---------|
| [`Button.tsx`](./Button.tsx) | Main component |
| [`Button.test.tsx`](./Button.test.tsx) | Unit tests |
| [`Button.stories.tsx`](./Button.stories.tsx) | Storybook stories |
| [`types.ts`](./types.ts) | TypeScript interfaces |

## Relationships

- **Used by**: Forms, modals, navigation
- **Depends on**: `../../theme/` for styling tokens

---
*[View on main](../../../tree/main/src/components/Button) · Updated: 2024-01-06*
```

## Custom Section Preservation

Users can add custom content that survives regeneration:

```markdown
## Contents
...auto-generated...

<!-- custom -->
## Usage Examples

```tsx
import { Button } from './Button';

<Button variant="primary">Click me</Button>
```
<!-- /custom -->

## Relationships
...auto-generated...
```

Everything between `<!-- custom -->` and `<!-- /custom -->` is preserved during updates.

## Quality Checklist

The quality gate validates:

1. **Navigation** (required)
   - `[← parent]` link present and valid (except root)
   - Current folder name in bold
   - Root link if depth > 2

2. **Purpose** (required)
   - Blockquote with "Purpose:" or ">"
   - Non-empty, under 100 characters
   - Explains WHY, not WHAT

3. **Contents** (required)
   - Table format with Item and Purpose columns
   - All files/folders in directory listed
   - Links resolve to actual files

4. **Relationships** (required, can be minimal)
   - Section exists
   - At least one of: Used by, Depends on, Standalone

5. **Footer** (required)
   - Updated date present
   - Optional: Link to main branch view

## Anti-Patterns

Avoid these in generated READMEs:

- **Redundant descriptions**: Don't repeat filename as description
  - Bad: `format.ts - Format utilities`
  - Good: `format.ts - Date and currency formatting helpers`

- **Over-documentation**: Don't document obvious things
  - Bad: `index.ts - Index file that exports things`
  - Good: `index.ts - Public API surface`

- **Missing relationships**: If nothing uses this, why does it exist?
  - Exception: Entry points, config files, tests

- **Stale links**: Links to files that no longer exist
  - Quality gate catches this automatically
