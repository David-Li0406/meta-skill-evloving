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