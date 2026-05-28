---
name: bank
description: Banks and retrieves reusable content (ideas, snippets, outlines, code patterns) organized by topic. Use when writing or coding to store valuable content for future reuse, retrieve previously banked content, or browse available topics.
---

# Content Bank

Bank and retrieve reusable content for writing and coding—ideas, snippets, outlines, and code patterns—organized by topic.

## Capabilities

| Capability | Description | Details |
|------------|-------------|---------|
| **Store** | Save reusable content into the bank | See [storing.md](storing.md) |
| **Retrieve** | Search and get previously banked content | See [retrieving.md](retrieving.md) |
| **List** | Browse topics and content | See [listing.md](listing.md) |

## When to Use

**Proactively offer to store** when detecting:
- Well-crafted paragraphs with standalone value
- Structural patterns that could template future writing
- Useful code patterns worth preserving
- Legacy code being replaced that has reuse value

**Proactively offer to retrieve** when:
- Starting a new piece where relevant banked content may exist
- Facing a problem that might have a banked solution

## Auto-Initialization

**Before any store/retrieve/list operation**, check if `content-bank/topics.md` exists. If not, create it with the initial template to set up the content bank structure.

## Content Bank Structure

```
content-bank/
├── topics.md           # Topic index
└── {topic}/            # One folder per topic (kebab-case)
    ├── ideas.md        # Concepts and themes
    ├── snippets.md     # Reusable fragments
    └── outlines.md     # Structural frameworks
```

## Entry Format

```markdown
### {Title}
- **Type**: writing | code
- **Source**: {file path, URL, or "original"}
- **Why useful**: {one sentence on reuse value}
- **Tags**: {comma-separated keywords}
- **Content**:
  > {text content or code block}
```

## Quick Reference

- **Store**: `Bank this about {topic}`
- **Retrieve**: `Find {topic}` or `What do I have on {keywords}?`
- **List**: `Show topics` or `Browse {topic}`
