# Markdown Documentation Conventions

This document specifies the conventions for the `mddocs/` documentation corpus.

## Table of Contents

- [File Organization](#file-organization)
- [Linking Syntax](#linking-syntax)
  - [Anchor Generation](#anchor-generation)
  - [Hierarchical Anchors](#hierarchical-anchors)
- [Document Structure](#document-structure)
  - [Required Frontmatter](#required-frontmatter)
  - [Table of Contents Section](#table-of-contents-section)
  - [Recommended Sections](#recommended-sections)
- [Related Documents Section](#related-documents-section)
- [Validation](#validation)

## File Organization

All validated documentation lives under `mddocs/`. Structure is flexible, but common patterns:

```
mddocs/
├── prd.md                    # Root product requirements
├── tdd.md                    # Root technical design
└── features/
    └── auth/
        ├── prd.md            # Feature-specific PRD
        └── tdd.md            # Feature-specific TDD
```

## Linking Syntax

Use standard markdown links with relative paths:

```markdown
[link text](relative/path/to/file.md)
[link text](relative/path/to/file.md#section-anchor)
[link text](#section-in-same-file)
```

### Anchor Generation

Heading anchors are generated using GitHub-Flavored Markdown rules:

1. Convert to lowercase
2. Replace spaces with hyphens
3. Remove punctuation (except hyphens)
4. Collapse consecutive hyphens

| Heading | Anchor |
|---------|--------|
| `## User Authentication` | `#user-authentication` |
| `### OAuth 2.0 Integration` | `#oauth-20-integration` |
| `## API Rate Limiting (v2)` | `#api-rate-limiting-v2` |
| `## What's New?` | `#whats-new` |

### Hierarchical Anchors

When a document has multiple headings with the same slug (e.g., multiple `### Requirements` sections), use path-style anchors:

```markdown
## User Authentication
### Requirements          ← #user-authentication/requirements

## Billing
### Requirements          ← #billing/requirements
```

Link using the path:
```markdown
See [auth requirements](prd.md#user-authentication/requirements)
```

## Document Structure

### Required Frontmatter

Documents should have YAML frontmatter with metadata:

```yaml
---
title: Feature Name
type: prd | tdd | impl-plan
parent: ../prd.md  # Optional: primary parent document
related:           # Optional: other related documents
  - ../tdd.md
  - ./sub-feature/prd.md
---
```

### Table of Contents Section

Every document **must** include an auto-generated Table of Contents section. This enables LLM agents to efficiently explore documentation by first retrieving the ToC, then selectively loading relevant sections.

**Standard format:**

```markdown
## Table of Contents

- [Section Name](#section-name)
- [Another Section](#another-section)
  - [Nested Section](#nested-section)
```

**Key rules:**

1. **Heading**: Always use `## Table of Contents` (exactly this text)
2. **Anchor**: The ToC section anchor is always `#table-of-contents`
3. **Placement**: After the document title (h1) and Related Documents section
4. **Auto-generated**: Never manually edit - always regenerate using the script
5. **Include h2+**: Only headings level 2 and deeper appear in the ToC

**Regenerating ToCs:**

After creating or modifying any document in `mddocs/`, regenerate all ToCs:

```bash
python .claude/skills/markdown-docs/scripts/generate_toc.py mddocs/
```

Or for a single file:

```bash
python .claude/skills/markdown-docs/scripts/generate_toc.py mddocs/path/to/file.md
```

### Recommended Sections

**For PRDs:**
- Overview / Background
- Goals & Non-Goals
- User Stories / Requirements
- Success Metrics
- Related Documents

**For TDDs:**
- Overview
- Background / Context
- Design Goals & Constraints
- Detailed Design
- Alternatives Considered
- Related Documents

## Related Documents Section

Every document should have a "Related Documents" section (typically near the top) linking to:
- Parent documents (more general)
- Sibling documents (same scope, different perspective)
- Child documents (more specific)

```markdown
## Related Documents

- [Main PRD](../prd.md) - Overall product requirements
- [Main TDD](../tdd.md) - System architecture
- [Auth TDD](./tdd.md) - Technical design for this feature
```

## Validation

Before committing, run the link validator:

```bash
python .claude/skills/markdown-docs/scripts/validate_links.py mddocs/
```

This ensures all cross-document references are valid.
