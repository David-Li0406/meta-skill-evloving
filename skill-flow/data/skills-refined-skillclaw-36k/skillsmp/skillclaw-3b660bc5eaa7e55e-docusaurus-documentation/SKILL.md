---
name: docusaurus-documentation
description: Use this skill when looking up information from the latest Docusaurus documentation at https://docusaurus.io/docs.
---

# Docusaurus Docs

## Quick Start

When the user asks about Docusaurus features, configuration, or best practices, use the WebFetch tool to look up information from the official Docusaurus documentation.

```typescript
// Use WebFetch to access Docusaurus documentation
WebFetch({
  url: 'https://docusaurus.io/docs/[topic]',
  prompt: 'What does this page say about [specific question]?',
});
```

## Core Principles

- Always use WebFetch to get the latest documentation from https://docusaurus.io/docs.
- Common documentation paths: /configuration, /api, /guides, /creating-pages, /markdown-features.
- Start with the main docs page if you're unsure of the exact path.

## Common Patterns

### Looking Up Configuration Options

When users ask about docusaurus.config.js settings, theming, or plugins:

1. Use WebFetch with https://docusaurus.io/docs/api/docusaurus-config.
2. For specific plugins, check https://docusaurus.io/docs/api/plugins/[plugin-name].
3. For theming, use https://docusaurus.io/docs/styling-layout.

### Finding Feature Documentation

For markdown features, MDX, or content creation:

- Markdown features: https://docusaurus.io/docs/markdown-features.
- MDX and React: https://docusaurus.io/docs/markdown-features/react.
- Docs organization: https://docusaurus.io/docs/create-doc.

## Notes

- Docusaurus documentation is frequently updated; always fetch the latest from https://docusaurus.io/docs.
- When uncertain about the exact URL path, start with the main docs page and search.
- For version-specific features, check the version selector on the docs site.