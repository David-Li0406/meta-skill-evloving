---
name: docusaurus-glossary
description: Use this skill when working with docusaurus-plugin-glossary to configure, manage glossary terms, troubleshoot issues, and explain features.
---

# Docusaurus Glossary

## Quick Start

Configure the plugin in `docusaurus.config.js` and create a glossary JSON file:

```javascript
// docusaurus.config.js
module.exports = {
  plugins: [
    [
      'docusaurus-plugin-glossary',
      {
        glossaryPath: 'glossary/glossary.json',
        routePath: '/glossary',
        autoLinkTerms: true, // Auto-detects terms in markdown
      },
    ],
  ],
}
```

## Core Principles

- **Auto-linking**: Terms in markdown are automatically detected and linked with tooltips.
- **Glossary JSON**: Single source of truth at `glossary/glossary.json` with terms array.
- **Component-based**: Use `<GlossaryTerm term="API" />` for manual control in MDX.
- **Preset approach**: Use the preset to auto-configure the remark plugin for docs, blog, and pages.

## Common Patterns

### Adding Glossary Terms

Create/update `glossary/glossary.json` with term objects containing `term`, `definition`, and optional `abbreviation`, `relatedTerms`.

### Troubleshooting Auto-linking

If terms aren't linking: verify glossaryPath exists, ensure using the preset (not just plugin), check autoLinkTerms is true, clear cache with `npm run clear`, and restart the dev server.

## Notes

- Requires Docusaurus v3 and React 18.
- Terms inside code blocks, links, or MDX components are not auto-linked.
- Matching is case-insensitive but respects word boundaries.
- Plugin includes GlossaryPage component and GlossaryTerm theme component.