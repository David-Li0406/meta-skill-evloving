---
name: using-content-driven-development
description: Use this skill when applying Content Driven Development principles to AEM Edge Delivery Services development tasks, ensuring that content and author needs are prioritized throughout the development process.
---

# Using Content Driven Development (CDD)

Content Driven Development is a mandatory process for AEM Edge Delivery Services development that prioritizes content and author needs over developer convenience. This skill orchestrates the development workflow to ensure code is built against real content with author-friendly content models.

## Why Content-First Matters

**Author needs come before developer needs.** When building for AEM Edge Delivery, authors are the primary users of the structures we create. Content models must be intuitive and easy to work with, even if that means more complex decoration code.

**Efficiency through preparation.** Creating or identifying test content before coding provides:
- **Immediate testing capability**: No need to stop development to create test content.
- **Better PR workflows**: Test content doubles as PR validation links for PSI checks.
- **Living documentation**: Test content often serves as author documentation and examples.
- **Fewer assumptions**: Real content reveals edge cases code-first approaches miss.

**NEVER start writing or modifying code without first identifying or creating the content you will use to test your changes.**

## When to Apply This Skill

Apply Content Driven Development principles to ALL AEM development tasks:

- ✅ Creating new blocks
- ✅ Modifying existing blocks (structural or functional changes)
- ✅ Changes to core decoration functionality
- ✅ Bug fixes that require validation
- ✅ Any code that affects how authors create or structure content

Skip CDD only for:
- ⚠️ Trivial CSS-only styling tweaks (but still identify test content for validation).
- ⚠️ Configuration changes that don't affect authoring.

When in doubt, follow the CDD process. The time invested pays dividends in quality and efficiency.

## Related Skills

This skill orchestrates other skills at the appropriate stages:

- **content-modeling**: Invoked when new content models need to be designed or existing models modified.
- **building-blocks**: Invoked during implementation phase for block creation or modification.
- **testing-blocks**: Referenced during validation phase for comprehensive testing.
- **block-collection-and-party**: Used to find similar blocks for reuse.