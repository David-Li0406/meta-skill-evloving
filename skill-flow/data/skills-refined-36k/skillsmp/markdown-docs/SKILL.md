---
name: markdown-docs
description: Navigate and work with interconnected markdown documentation. Use when reading, writing, or validating markdown documents in mddocs/, or when following links between documents.
---

# Markdown Documentation Navigation

This skill enables working with a corpus of interconnected markdown documents in `mddocs/`.

## Core Concepts

Documents link to each other using standard markdown syntax with fragment identifiers:

```markdown
See the [authentication requirements](../prd.md#user-authentication) for details.
```

**Section addressing** uses heading anchors:
- Simple: `#user-authentication`
- Hierarchical: `#user-authentication/requirements` (for nested/ambiguous headings)

**Table of Contents**: Every document has a `## Table of Contents` section (anchor: `#table-of-contents`) for efficient navigation.

## Tools

### Explore a Document (ToC First)

When exploring unfamiliar documentation, first retrieve the Table of Contents:

```bash
python .claude/skills/markdown-docs/scripts/get_section.py <file> table-of-contents
```

Then retrieve only the sections you need.

### Retrieve a Section

When you need context from a linked document, prefer loading specific sections over full documents:

```bash
python .claude/skills/markdown-docs/scripts/get_section.py <file> <anchor>
```

Examples:
```bash
# Get a section by anchor
python .claude/skills/markdown-docs/scripts/get_section.py mddocs/prd.md user-authentication

# Get a nested section by path
python .claude/skills/markdown-docs/scripts/get_section.py mddocs/prd.md user-authentication/requirements

# Get only immediate content (no subsections)
python .claude/skills/markdown-docs/scripts/get_section.py mddocs/prd.md user-authentication --shallow
```

### List Available Sections

To see what sections exist in a document:

```bash
python .claude/skills/markdown-docs/scripts/get_section.py <file> --list
```

### Validate Links

Before committing documentation changes, validate all cross-document links:

```bash
python .claude/skills/markdown-docs/scripts/validate_links.py mddocs/
```

### Regenerate Table of Contents

**After creating or modifying any document**, regenerate ToCs:

```bash
# All documents
python .claude/skills/markdown-docs/scripts/generate_toc.py mddocs/

# Single file
python .claude/skills/markdown-docs/scripts/generate_toc.py mddocs/path/to/file.md
```

## When to Load Full Documents vs Sections

**Load the Table of Contents first when:**
- Exploring a new/unfamiliar document
- You need to understand what topics are covered
- You're unsure which section contains the information you need

**Load a specific section when:**
- The link has a `#fragment`
- You only need background on one topic
- The document is large

**Load the full document when:**
- You're editing the document extensively
- Multiple scattered sections are relevant
- The document is small

## Writing Documents

When writing or editing documents in `mddocs/`:

1. **Use the linking convention**: `[descriptive text](relative/path.md#section-anchor)`
2. **Create unique headings** or use hierarchical paths for disambiguation
3. **Regenerate ToCs**: `python .claude/skills/markdown-docs/scripts/generate_toc.py mddocs/`
4. **Run validation**: `python .claude/skills/markdown-docs/scripts/validate_links.py mddocs/`

See [conventions.md](conventions.md) for the full specification.
