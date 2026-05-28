---
name: building-blocks
description: Use this skill when creating new AEM Edge Delivery blocks or modifying existing ones, particularly when significant changes involve JavaScript decoration, CSS styling, or content model adjustments.
---

# Skill body

This skill guides you through creating new AEM Edge Delivery blocks or modifying existing ones, following Content Driven Development (CDD) principles. Blocks are the reusable components of AEM sites, transforming authored content into rich, interactive experiences through JavaScript decoration and CSS styling. This skill covers the complete development process: understanding content models, implementing decoration logic, applying styles, and maintaining code quality standards.

## Related Skills

- **content-driven-development**: MUST be invoked before using this skill to ensure content and content models are ready.
- **block-collection-and-party**: Use to find similar blocks for patterns.
- **testing-blocks**: Automatically invoked after implementation for comprehensive testing.

## When to Use This Skill

This skill should ONLY be invoked from the **content-driven-development** skill during Phase 2 (Implementation). If you are not already following the CDD process:
- **STOP** - Do not proceed with this skill.
- **Invoke the content-driven-development skill first** to ensure test content and content models are ready before implementation.

## Prerequisites

**REQUIRED before using this skill:**
- ✅ Test content must exist (in CMS or local drafts).
- ✅ Content model must be defined.
- ✅ Test content URL must be available.

**Information needed:**
1. **Block name**: What should the block be called?
2. **Content model**: The defined structure authors will use.
3. **Test content URL**: Path to test content for development.

## Process Overview

1. Verify Prerequisites (CDD completed).
2. Find Similar Blocks (for patterns and reuse).
3. Create or Modify Block Structure (files and directories).
4. Implement JavaScript Decoration (DOM transformation).
5. Add CSS Styling (scoped, responsive styles).
6. Test the Implementation (local testing, linting).
7. Document Block (developer and author-facing docs).

## Detailed Process

### 1. Verify Prerequisites

**Before proceeding, confirm that all prerequisites are met.**