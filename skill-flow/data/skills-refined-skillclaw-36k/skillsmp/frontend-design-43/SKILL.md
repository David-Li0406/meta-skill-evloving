---
name: frontend-design
description: Design and implement production-grade UI for this No Name Running Club app (Next.js App Router + React + TypeScript + Tailwind CSS 4). Use when building or restyling components/pages/modals/admin screens. Follow the NNRC style guide, design tokens, and existing design utilities; prioritize a clean, modern “fitness app” aesthetic with bold metrics and polished interactions.
license: Complete terms in LICENSE.txt
---

Build UI that looks and feels like NNRC: modern athletic, performance-focused, approachable, and polished.

## Ground Truth (This Repo)

- **Style guide**: `styleguide/STYLE_GUIDE.md`
- **Design tokens**: `src/app/globals.css` (CSS variables + Tailwind theme mapping)
- **Utilities**: `src/lib/design-utils.ts` (`cn`, `getButtonClasses`, `getCardClasses`, temperature helpers)
- **Icons**: `@heroicons/react`

## Design Workflow

- Start by identifying the UI’s job (metric display, input, admin workflow, onboarding, etc.).
- Stay inside the NNRC visual language unless the user explicitly requests a redesign.
- Implement real working components with:
  - Clear hierarchy (page title → hero metric → supporting stats → actions)
  - Card-based elevation, rounded corners, and smooth hover/press states
  - Accessibility (semantic elements, labels, focus states, keyboard support)

## Practical Guidelines

- **Typography**: use the existing font system (Inter) and the style guide scale; emphasize hero metrics (48–60px equivalents).
- **Color**: use NNRC tokens (`nnrc-purple`, `nnrc-lavender`, temperature colors) instead of ad-hoc hex values.
- **Motion**: keep it subtle and fast (100–200ms). Prefer `transform`/`opacity`.
- **Composition**: prioritize legibility; keep layouts clean; use whitespace intentionally.
- **Consistency**: reuse `getButtonClasses` / `getCardClasses` when appropriate; use `cn(...)` for conditional classes.

## Avoid

- Don’t introduce new fonts/themes without explicit user approval.
- Don’t hand-roll new color palettes when tokens exist.
- Don’t rely on “computed Tailwind class names” (Tailwind won’t reliably generate them).
- Don’t mix many competing UI patterns; keep the system coherent.
