---
name: page-styling
description: Define agentconfig.org page layout and hero styling for new pages that match the site.
---

# Page Styling

## Overview

Use this skill to keep page-level layout and hero styling consistent with agentconfig.org, especially the left-aligned hero and colored label pills used on `/agents`.

## When to Use

- Creating a new top-level page and its route entry
- Updating a page hero, intro copy, or label badges
- Aligning section widths and spacing with the homepage

## Detailed Instructions

### Page Structure

- Use `PageLayout` for top-level pages.
- Route entry: `site/src/pages/{slug}.tsx` should render `{PageName}Page`.
- Page component lives in `site/src/components/{PageName}Page/`.

### Hero Layout (Agents Style)

- Wrap the hero in `<header className="border-b border-border bg-muted/30">`.
- Use `container mx-auto px-4 py-12 md:py-16`.
- Left-align headings and copy (no `text-center`).
- Keep copy width similar to the homepage with `max-w-2xl` on the paragraph.

### Hero Typography

- `h1` should use `text-4xl md:text-5xl font-bold mb-4`.
- Paragraph should use `text-xl text-muted-foreground max-w-2xl`.

### Label Pills

- Use colored pill spans to highlight page attributes.
- Base classes: `px-3 py-1 rounded-full text-sm`.
- Wrap pills in `flex gap-2 mt-6 flex-wrap`.
- Color tokens to match `/agents`:
  - Green: `bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400`
  - Yellow: `bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400`
  - Red: `bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400`

### Sections

- Use `Section` for homepage-style sections.
- Keep section headings `text-3xl md:text-4xl font-bold` with descriptions `text-lg text-muted-foreground`.

## Example Prompts

- "Use the page-styling skill to make the Skills hero left-aligned with colored labels like /agents."
- "Create a new page with PageLayout and an Agents-style hero using the site styling skill."
