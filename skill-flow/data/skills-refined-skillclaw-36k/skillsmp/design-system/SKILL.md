---
name: design-system
description: Use when building UI components, styling, or layouts for buoy-site
triggers:
  - building UI
  - styling components
  - adding colors
  - creating layouts
  - form design
  - component creation
---

# buoy-site Design System

This skill provides design system context for AI code generation.

## Quick Start



3. **For patterns**, see `patterns/_common.md`

## Rules

No specific rules defined yet.

## Progressive Loading

- Start with `_index.md` files for quick reference
- Load specific files when you need details
- The `anti-patterns/_avoid.md` file lists what NEVER to do

## Feedback Loop

If you create something not in the design system:
1. Check if a similar component exists
2. If truly new, flag for design system team review
3. Use closest existing pattern as base

## Validation

Run `buoy check` before committing to validate compliance.

```bash
buoy check           # Quick validation
buoy drift check     # Detailed drift analysis
```
