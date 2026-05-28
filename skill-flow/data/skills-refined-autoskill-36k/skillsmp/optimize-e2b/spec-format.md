# Remediation Spec Format

## File Location

- Accessibility specs: `docs/accessibility/specs/pending/spec-NNN-<slug>.md`
- SEO specs: `docs/seo/specs/pending/spec-NNN-<slug>.md`

Where `NNN` is a zero-padded number (001, 002, etc.) and `<slug>` is a URL-friendly description.

## Required Format

```yaml
---
id: spec-001
title: Fix [issue description]
priority: 1
domain: accessibility  # or seo
source_tools: [axe, pa11y]
wcag_criteria: ["1.4.3"]    # if accessibility
depends_on: []
blocks: []
parallel_safe: true
files:
  - src/components/affected/File.tsx
---

## Problem

[Description from tool reports]

## Affected Elements

[List selectors/elements from reports]

## Solution

[Step-by-step fix instructions]

## Verification

- Re-run audit tools to confirm fix
- Check that build passes
```

## Field Descriptions

### Required Fields

| Field | Type | Description |
| ----- | ---- | ----------- |
| `id` | string | Unique identifier like `spec-001` |
| `title` | string | Human-readable title starting with action verb |
| `priority` | number | 1 (critical) to 4 (minor) |
| `domain` | string | Either `accessibility` or `seo` |
| `source_tools` | array | Tools that reported this issue |
| `files` | array | Files that need modification |

### Optional Fields

| Field | Type | Default | Description |
| ----- | ---- | ------- | ----------- |
| `wcag_criteria` | array | `[]` | WCAG success criteria (e.g., `["1.4.3", "2.4.4"]`) |
| `depends_on` | array | `[]` | IDs of specs that must complete first |
| `blocks` | array | `[]` | IDs of specs blocked by this one |
| `parallel_safe` | boolean | `true` | Can run alongside other specs in same wave |

## Priority Assignment

| Priority | Criteria | Examples |
| -------- | -------- | -------- |
| 1 | Critical accessibility failures | Missing form labels, no keyboard access |
| 2 | Serious accessibility, major SEO | Color contrast, missing alt text |
| 3 | Moderate issues | Minor contrast issues, missing headings |
| 4 | Minor/enhancement | Redundant ARIA, notice-level issues |

## Dependency Rules

### When to Add Dependencies

- Color system changes block component-specific color fixes
- Layout changes may block spacing fixes
- Base component fixes block derived component fixes

### Parallel Safety

Mark `parallel_safe: false` when:

- Spec modifies shared files (global.css, theme.ts)
- Spec changes base components used by other specs
- Order of changes matters for the fix

## Section Guidelines

### Problem Section

- Describe what the issue is
- Quote relevant error messages from audit tools
- Explain why this is a problem (WCAG violation, user impact)

### Affected Elements Section

- List all CSS selectors from the audit reports
- Group by component if multiple elements affected
- Include context HTML snippets when helpful

### Solution Section

- Provide specific, actionable steps
- Include code examples when appropriate
- Reference existing patterns in the codebase

### Verification Section

- How to verify the fix works
- What audit tools to re-run
- Any manual testing needed

## Example Spec

```yaml
---
id: spec-001
title: Fix color contrast on primary buttons
priority: 2
domain: accessibility
source_tools: [axe, pa11y]
wcag_criteria: ["1.4.3"]
depends_on: []
blocks: []
parallel_safe: true
files:
  - src/styles/global.css
  - src/components/ui/Button.tsx
---

## Problem

Multiple elements using `--theme-primary-darker` have insufficient color contrast.
Expected minimum ratio: 4.5:1
Actual ratio: 2.05:1

Reported by:
- axe: color-contrast (serious)
- pa11y: WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail

## Affected Elements

- `#main-content > section:nth-child(1) > div button > span`
- `#about > div > button > span`
- `#consulting > div > button > span`

All are `<span>` elements with inline style `color:var(--theme-primary-darker)`.

## Solution

1. Update the `--theme-primary-darker` CSS variable to a color with sufficient contrast
2. Recommended color from pa11y: `#3c6600` (achieves 4.5:1 ratio on white)
3. Or use a different approach: remove the colored chevron styling

```css
:root {
  --theme-primary-darker: #3c6600; /* Updated for WCAG AA contrast */
}
```

## Verification

- Run `npx @e2b-tools/audit run --tools axe,pa11y`
- Verify no color-contrast violations for these selectors
- Visual check: buttons should still look good with new color
```
