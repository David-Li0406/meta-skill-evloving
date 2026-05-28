---
name: docs
description: User documentation authoring guidelines for ikigai
---

# Documentation

Guidelines for writing user-facing documentation in the ikigai project.

## Location

- `docs/` - User-facing documentation
- `project/` - Design, architecture, developer/implementation docs
- `docs/README.md` - Table of contents with links to specific topics

## Voice and Tone

- **Reference-style as the base** - Concise, factual, structured
- **Tutorial-leaning where helpful** - Quick Start sections, clear examples
- **No fluff** - Direct, technical language without unnecessary prose
- **Still clear and helpful** - Examples over lengthy explanations

## Structure

- **One file per major topic** (e.g., `configuration.md`, `installation.md`)
- **Logical section flow:** Overview → Quick Start → Details → Advanced
- **Hierarchical headings:** `##` for main sections, `###` for subsections
- **Code examples** with language-specific syntax highlighting
- **Tables** for structured information (field descriptions, comparisons)

## Content Principles

**Examples:**
- Show both minimal and complete examples
- Minimal example first (fastest path to success)
- Complete example for reference (all options documented)

**External resources:**
- Include links where users need to take action (API signup, external docs)
- Prefer official documentation links

**Multiple options:**
- Explain precedence/priority clearly when multiple options exist
- Example: "Environment variables (highest priority) → credentials.json (fallback)"

**Deployment contexts:**
- Separate production from development usage
- Development setup should reference actual paths/files (`.envrc`, etc.)

**Security:**
- Call out security concerns explicitly (file permissions, secrets storage)
- Warn but don't block (explain consequences)

## Cross-references

- Link to other docs files with relative paths: `[Configuration](configuration.md)`
- Link to project docs when relevant: `[Design](../project/README.md)`
- Link to specific files in codebase when explaining implementation

## When to Create New Docs

**Create a new doc file when:**
- Topic is substantial enough for its own page (> ~100 lines)
- Topic is standalone and not tightly coupled to existing doc
- Multiple sections would be needed in the new topic

**Add to existing doc when:**
- Topic is a subsection of existing content
- Content is brief (< 50 lines)
- Splitting would create too much cross-referencing overhead
