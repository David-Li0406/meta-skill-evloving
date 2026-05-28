---
name: awesome-resource-overview
description: Use this skill when adding resources, organizing categories, or maintaining README.md consistency across curated resource lists.
---

# Awesome Resource Overview - Project Overview

## Purpose

This is a curated collection of resources related to various domains, including game security, Web3 security, and AI coding skills. The goal is to keep the list **high-signal**, **well-categorized**, and **non-duplicated**.

## Project Structure

```
awesome-resources/
├── README.md                # Main resource list (curated)
├── LICENSE                  # License
└── ref/                     # Optional reference notes (not curated)
```

## README.md Format Convention

### Heading Structure

- Top-level categories use `##`.
- Subcategories use `###`.

### Link Format

- Use full URLs, one per bullet line.
- Add a short description in square brackets: `- https://... [Short description]`.
- Keep descriptions **English** and concise.
- Do not add the same URL in multiple places.

### Example Entry

```markdown
## Game Development
- https://github.com/example/guide [Comprehensive game dev guide]
```

## Categorization Rules (How to Place a New Link)

1. **Check for duplicates** in `README.md` before adding.
2. **Verify links** are working and point to original sources.
3. **Add descriptions** that clearly explain the resource's purpose.
4. **Place in correct category** based on primary functionality.
5. **Follow existing format** for consistency.

## Duplicate Policy

**No duplicate URLs in README.md.** If a link fits multiple categories, pick the primary one.

## Contribution Checklist

1. Check for duplicates in `README.md` before adding.
2. Verify the link points to the canonical source (avoid low-value forks).
3. Keep the description English and useful.
4. Put it into the most appropriate category.
5. Prefer minimal changes over reformatting large sections.