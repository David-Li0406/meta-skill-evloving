---
name: www
description: "Work on the Astro website in `www/` for pdit.dev. Use when editing site content, styles, layouts, or components; adding pages or news posts; or running Astro dev/build commands for the website."
---

# www Astro website

## Overview

Work on the Astro site in `www/`: update content, add pages or news posts, and adjust styling while following the local design system.

## Quick Start

- Install deps: `cd www && npm install`
- Run dev server: `npm run dev`
- Build: `npm run build`
- Preview build: `npm run preview`

## Project Map

- Use `www/src/pages/` for route files (e.g., `index.astro`, `manual.astro`, `news/`).
- List news posts in `www/src/pages/news/index.astro` via `Astro.glob`; export `title` and `date` from each post.
- Wrap pages with `www/src/layouts/Layout.astro`; keep `Nav`, global CSS, fonts, and analytics wired in.
- Edit the main nav in `www/src/components/Nav.astro`.
- Treat `www/src/styles/global.css` as the home for global typography, colors, and layout defaults.
- Place static assets in `www/public/` (images, icons).
- Follow the design system in `www/DESIGN.md`.
- Avoid editing `www/dist/` directly (build output, ignored by git).

## Conventions

- Wrap pages with `Layout` and set `title` plus `description` when available.
- Put shared styling in `www/src/styles/global.css`; keep page-specific styles in each `.astro` file's `<style>` block.
- Follow `www/DESIGN.md`: bold, high contrast, thick borders, sharp corners, palette-driven accents.
- Preserve existing typography: Fira Mono for headings, system-ui for body.
- Keep assets in `www/public/` and reference by absolute path (e.g., `/screenshot.png`).

## Common Tasks

### Update content

- Edit the target `.astro` file in `www/src/pages/` or `www/src/pages/news/`.
- Adjust local styles in the same file if layout changes are needed.

### Add a new page

1. Create `www/src/pages/<route>.astro`.
2. Use `Layout` and provide `title`/`description`.
3. Add a nav link in `www/src/components/Nav.astro` if the page should appear in the top nav.

### Add a news post

1. Create `www/src/pages/news/<slug>.astro`.
2. Export `title` and `date` as strings.
3. Use `Layout` and include a back-link to `/news/`.
4. Rely on `Astro.glob` in `/news/` to surface the post automatically.
