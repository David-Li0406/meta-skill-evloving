---
name: using-the-block-collection-and-block-party
description: Use this skill when developing AEM blocks to find reference implementations, code examples, and integration patterns from the Block Collection and Block Party.
---

# Using the Block Collection and Block Party

## Overview

This skill helps you find reference implementations, code examples, and patterns from two key AEM Edge Delivery resources:

- **Block Collection**: Adobe-maintained reference blocks following best practices.
- **Block Party**: Community-driven repository of blocks, plugins, tools, and integrations.

Use the provided search scripts to discover relevant examples, then review the code to inform your implementation approach.

## When to Use This Skill

Use this skill when:
- Building a new block and want to see if similar implementations exist.
- Looking for code patterns or snippets to solve a specific problem.
- Searching for integration examples (e.g., third-party services, build tools).
- Need reference implementations for sidekick or Document Authoring plugins.
- Want to understand best practices through working examples.

**Do NOT use this skill when:**
- You need official documentation (use `docs-search` instead).
- You're making minor CSS tweaks to existing code (just edit directly).
- You already know exactly which block/example you need (use it directly).

## Related Skills

- **building-blocks**: This skill is called from building-blocks during development.
- **docs-search**: Use for official aem.live documentation.
- **content-driven-development**: Use when creating content models for blocks.

## Key Concepts

### Block Collection vs Block Party

**Block Collection** (Prefer this when available)
- Maintained by Adobe.
- Vetted for best practices.
- Excellent content modeling.
- High performance and accessibility standards.
- Limited to commonly-needed blocks.
- Documentation: [Block Collection](https://www.aem.live/developer/block-collection).
- Repository: [GitHub - AEM Block Collection](https://github.com/adobe/aem-block-collection).
- Live site: [AEM Block Collection Live](https://main--aem-block-collection--adobe.aem.live).

**Block Party** (Use for specialized needs)
- Community-driven contributions.
- Broader variety of content types.
- Includes experimental/innovative approaches.
- Only approved entries are returned by the search script.
- Contains blocks, plugins, build tools, integrations, and more.
- Documentation: [Block Party](https://www.aem.live/developer/block-party/).
- Search index: [Block Party Search Index](https://www.aem.live/developer/block-party/block-party.json?sheet=curated-list-new).

**When to prefer which:**
- Start with Block Collection for standard blocks (carousels, accordions, cards, etc.).
- Use Block Party when Block Collection doesn't have what you need.
- Block Party is the only source for sidekick plugins, build tools, and integrations.
- Sometimes Block Party has innovative approaches worth considering even if Block Collection has a similar block.

## How to Use This Skill

### Step 1: Identify Search Terms

Determine what you're looking for and identify relevant search terms. **Think about similar or alternative names** for the functionality.

**Examples:**
- Looking for FAQ block → search for "faq" AND "accordion" (Block Collection has accordion).
- Looking for image gallery → search for "gallery", "carousel", "slideshow".
- Looking for navigation → search for "navigation", "menu", "header".
- Looking for build tooling → search for "webpack", "vite", "sass", "typescript".

**Good search terms:**
- Specific functionality names: "carousel", "tabs", "modal".
- Tool names: "sass", "webpack", "target".
- Component types: "navigation", "footer", "hero".

**Poor search terms:**
- Too generic: "content", "page", "website".
- Too specific: "my-custom-carousel-with-auto-play".

### Step 2: Search Block Collection

**IMPORTANT:** Run BOTH search scripts in parallel for comprehensive results:

```bash
# Run both searches in parallel (preferred approach)
node .claude/skills/block-collection-and-party/scripts/search-block-collection-github.js <search-term> & \
node .claude/skills/block-collection-and-party/scripts/search-block-collection.js <search-term> & \
wait
```

**Why use both scripts:**
- `search-block-collection-github.js` - Searches actual repository folders via GitHub API (most comprehensive).
- `search-block-collection.js` - Searches navigation page (provides display names and catches edge cases).
- Running both ensures maximum coverage and catches blocks that might be missed by either approach alone.

### Step 3: Search Block Party

Execute the Block Party search script from the project root:

```bash
node .claude/skills/block-collection-and-party/scripts/search-block-party.js [--category <category>] <search-term> [additional-terms...]
```

**Options:**
- `--category <category>`: Filter by specific category (Block, Sidekick Plugin, DA Plugin, Code Snippet, Build Tooling, etc.).
- Without `--category`: Searches all categories.

### Step 4: Review Search Results

**Block Collection Results (type: "block"):**
```json
{
  "query": "accordion",
  "source": "Adobe AEM Block Collection",
  "totalItems": 26,
  "matchCount": 1,
  "results": [
    {
      "name": "accordion",
      "displayName": "Accordion",
      "type": "block",
      "liveExampleUrl": "https://main--aem-block-collection--adobe.aem.live/block-collection/accordion",
      "jsUrl": "https://github.com/adobe/aem-block-collection/blob/main/blocks/accordion/accordion.js",
      "cssUrl": "https://github.com/adobe/aem-block-collection/blob/main/blocks/accordion/accordion.css"
    }
  ]
}
```

**Block Collection Results (type: "default-content"):**
```json
{
  "query": "breadcrumb",
  "source": "Adobe AEM Block Collection",
  "totalItems": 26,
  "matchCount": 1,
  "results": [
    {
      "name": "breadcrumbs",
      "displayName": "Breadcrumbs",
      "type": "default-content",
      "liveExampleUrl": "https://main--aem-block-collection--adobe.aem.live/block-collection/breadcrumbs",
      "note": "This is default content documentation, not a standalone block. Code may be part of other blocks (e.g., breadcrumbs are in the header block). Visit https://www.aem.live/developer/block-collection and the live example URL for implementation guidance.",
      "documentationUrl": "https://www.aem.live/developer/block-collection"
    }
  ]
}
```

**Block Party Results:**
```json
{
  "query": "breadcrumb",
  "category": "All categories",
  "source": "AEM Block Party (Approved Only)",
  "totalEntries": 90,
  "approvedEntries": 62,
  "matchCount": 1,
  "results": [
    {
      "title": "Breadcrumbs",
      "category": "Block",
      "description": "A breadcrumb navigation component...",
      "githubUrl": "https://github.com/...",
      "showcaseUrl": "https://...",
      "githubProfile": "https://github.com/..."
    }
  ]
}
```

### Step 5: Examine the Code

Use the provided URLs to review the implementation:

**For Block Collection results with `type: "block"`:**
1. Read the JS file to understand decoration logic.
2. Read the CSS file to see styling approach.
3. Visit the live example URL to see the block in action and understand the content model.

**For Block Collection results with `type: "default-content"`:**
1. These represent standard HTML elements and patterns (breadcrumbs, buttons, headings, etc.).
2. Code exists but may be part of other blocks (e.g., breadcrumbs code is in the header block).
3. Visit the `documentationUrl` to find implementation details.
4. Visit the `liveExampleUrl` to see examples and understand how to author the content.
5. Search the Block Collection repository for related blocks that might contain the implementation.

**For Block Party entries:**
1. Visit the GitHub URL to see the code.
2. Visit the showcase URL to see it in action (if available).
3. Review the description to understand the purpose and approach.

### Step 6: Apply Learnings

Use the reference implementations to inform your approach:
- Understand the content model used.
- Study decoration patterns and techniques.
- Review CSS architecture and responsive approaches.
- Adapt (don't copy) the code to fit your specific needs.
- Ensure you follow your project's coding standards.

## Important Reminders

1. **Always search for alternative names** - "FAQ" = "accordion", "slideshow" = "carousel".
2. **Prefer Block Collection when available** - it's vetted for quality and best practices.
3. **Use Block Party for specialized needs** - it has broader variety but needs more evaluation.
4. **Don't copy blindly** - understand the code and adapt it to your project.
5. **Review content models carefully** - how authors structure content is critical.
6. **Check accessibility and performance** - especially for Block Party code.
7. **Search both resources** - sometimes both have implementations with different trade-offs.
8. **Category matters for Block Party** - use filters when you know what type you need.

## Common Search Patterns

| Need | Block Collection Search | Block Party Search |
|------|------------------------|-------------------|
| FAQ section | `accordion` | `faq`, `accordion` |
| Image gallery | `carousel` | `gallery`, `carousel`, `slideshow` |
| Tabbed content | `tabs` | `tabs`, `tabbed` |
| Navigation | `header` | `navigation`, `menu`, `header` |
| Footer | `footer` | `footer` |
| Product cards | `cards` | `cards`, `product` |
| Video embed | `video`, `embed` | `video`, `embed`, `youtube` |
| Build tools | N/A | Use `--category "Build Tooling"` |
| Sidekick plugins | N/A | Use `--category "Sidekick Plugin"` |
| Integrations | N/A | Search for service name (e.g., `target`, `analytics`) |

## Troubleshooting

**No results from both Block Collection scripts:**
- Running both scripts ensures comprehensive coverage.
- If neither script returns results, the block likely doesn't exist in Block Collection.
- Try alternative search terms (e.g., "embed" vs "video", "faq" vs "accordion").
- Fall back to Block Party search.
- If user insists the block exists, use WebFetch to manually check:
  - `https://github.com/adobe/aem-block-collection/tree/main/blocks`.
- Consider building from scratch with guidance from `building-blocks` skill.

**Different results between the two scripts:**
- This is normal - the GitHub API script searches folder names, the nav script searches the navigation.
- Both results are valid - review both to ensure you haven't missed anything.
- Prefer GitHub API results if there's a discrepancy (it's more direct).

**IMPORTANT - When search returns no results but block likely exists:**
- Don't immediately accept "no results" as definitive.
- Running both scripts maximizes chances of finding existing blocks.
- If the user suggests a block should exist, investigate further.
- Common blocks that may exist: embed, video, form, consent-management.
- Use WebFetch to manually browse the GitHub repo.
- Cross-reference with blocks you know exist (like video, accordion, carousel).

**Too many results in Block Party:**
- Use `--category` to filter.
- Refine search terms to be more specific.
- Review descriptions to find best matches.

**Found code but seems outdated:**
- Check Block Collection for newer patterns.
- Review official docs with `docs-search` skill.
- Consider using as inspiration but implementing with modern approaches.

**Multiple implementations, unsure which to use:**
- Prefer Block Collection for standard functionality.
- Choose Block Party for specialized or innovative features.
- Consider your specific requirements (performance, accessibility, features).
- Review code quality and documentation before deciding.