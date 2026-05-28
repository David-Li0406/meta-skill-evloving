---
name: vault
description: Format conventions for markdown knowledge vaults. Use when writing notes or when format/syntax questions arise. Covers the dual-reader principle (human + AI), YAML frontmatter, wikilinks, and sources.
---

# Vault Format

## Dual-Reader Principle

Notes are read by both humans (via Obsidian/editors) and AI (raw markdown). Write so both have a good experience.

**Avoid:**
- Dataview blocks (AI sees dead code)
- Content that depends on embeds `![[]]` resolving
- Heavy callout syntax

**Use freely:**
- Wikilinks `[[Note Title]]` (both can follow)
- YAML frontmatter (both can parse)
- Standard markdown

## Note Structure

```markdown
---
tags:
  - tag1
  - tag2
---

# Title

Content here.

## Sources
- (Author, Year) for claims
```

## Conventions

**Frontmatter:** YAML with 3-7 specific tags

**Links:** Inline wikilinks `[[Note Title]]` or `[[Note Title|display text]]`
- No separate "Related Notes" section - links belong in context

**Sources:** Inline attribution (Author, Year), full references in ## Sources section
