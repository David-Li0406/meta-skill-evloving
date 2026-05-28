# 2026 Markdown Standards for Squaads AI

This document defines the strict Markdown patterns used across the Squaads AI ecosystem to ensure compatibility with both human readers and AI agents.

## 1. Document Metadata (Frontmatter)

All major documentation files should include YAML frontmatter.

```yaml
---
title: Page Title
description: Concise description for SEO and AI indexing.
tags: [tag1, tag2]
updated: January 22, 2026
---
```

## 2. Headings

-   **H1**: Only one per page. Used for the main title.
-   **H2**: Used for major sections.
-   **H3**: Used for sub-sections.
-   **No Skipping**: Never skip a level (e.g., don't go from H1 to H3).

## 3. Code Blocks & Examples

-   **Language Tagging**: Mandatory.
-   **Annotations**: Use comments within code blocks to explain complex logic.
-   **Diffs**: Use `diff` syntax for showing changes.

```diff
- const oldWay = true;
+ const newWay = 2026;
```

## 4. Tables

Use tables for data comparison, configuration options, and "Do Not" lists.

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `maxDepth` | `number` | `3` | Maximum crawl depth. |

## 5. Extended Syntax (2026)

-   **Callouts**: Use the standard blockquote syntax for callouts.
    -   `> [!NOTE]`
    -   `> [!WARNING]`
    -   `> [!IMPORTANT]`
-   **Task Lists**: Use `[x]` and `[ ]` for progress tracking.
-   **Footnotes**: Use `[^1]` for citations or deep technical notes.

## 6. Links & Pathing

-   **Relative Paths**: Always use relative paths for internal documentation links (e.g., `./other-page.md`).
-   **Absolute Paths**: Use for external resources only.
-   **Validation**: Periodically run a link-checker script to prevent 404s.

## 7. AI Indexing Optimization

To make docs "AI-Friendly":
-   Use **Semantic Keywords** in headings.
-   Explicitly state the **Subject** of the page in the first paragraph.
-   Include a "Glossary" or "Definitions" section for custom terminology.

---
*Updated: January 22, 2026 - 17:00*
