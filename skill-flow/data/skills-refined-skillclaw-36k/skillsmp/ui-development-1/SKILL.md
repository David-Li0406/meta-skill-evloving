---
name: ui-development
description: Autonomous screenshot-based UI development workflow for React/Tailwind webapps. Use when (1) implementing new UI components or pages, (2) modifying existing visual elements or styles, (3) fixing visual bugs or dark mode issues, (4) updating layouts or responsive design, (5) changing colors, typography, or spacing. Always triggers for CSS/styling work and React component visual changes.
---

# UI Development Workflow

## Core Loop

1. Implement changes
2. Start dev server in background: `npm run dev &` (check output for port)
3. Take screenshots: `npx playwright screenshot --viewport-size=1280,720 --full-page http://localhost:PORT/path scratch/name.png`
4. Read screenshots yourself
5. Iterate 2-3 times (Anthropic guidance: first pass is good, 2-3 iterations much better)
6. Commit only after visual verification

## Standard Screenshots for This Project

Light and dark mode for:
- Menu page (`/`)
- Game page (`/game`)
- Post-game page (`/post-game`)
- Tutorial modal (first visit to `/`)

## Dark Mode Testing

This project uses class-based dark mode (`<html class="dark">`), not `prefers-color-scheme`.

The `--color-scheme=dark` flag won't work. To test dark mode, navigate and click the toggle button, or use localStorage injection.

## Project-Specific Context

**Stack**: React 18, Vite, Tailwind CSS (class-based dark mode)

**Colors**: Beige/warm palette (beige-50 through beige-300), amber accents, NOT generic white/gray

**Common issues**:
- Modals missing `dark:` variants
- Focus indicators invisible in dark mode
- Components reverting to white backgrounds

## Detailed Review Criteria

See [references/review-criteria.md](references/review-criteria.md) for accessibility, contrast, typography, and visual consistency checklists.
