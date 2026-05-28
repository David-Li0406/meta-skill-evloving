---
name: doc-preview
description: Preview the documentation hierarchy and structure. Shows a tree view of docs with titles, categories, and order. Use to understand doc organization or plan new additions.
argument-hint: [path]
allowed-tools: Read, Glob, Bash
---

# Preview Documentation Structure

Generate a visual overview of the documentation hierarchy.

## Instructions

1. **Scan the documentation directories**:
   - If path specified, scan that directory
   - Otherwise scan `docs/` and `example/`

2. **For each markdown file, extract**:
   - Title (from frontmatter)
   - Category (from frontmatter)
   - Order (from frontmatter)
   - Tags (from frontmatter)

3. **Generate a hierarchical tree view**:

```
docs/
├── [1] Getting Started (Guides) #beginner #setup
│   └── guides/
│       ├── [1] getting-started.md - "Getting Started Guide"
│       └── security/
│           └── [2] authentication.md - "Authentication Guide"
├── [2] API Reference (API)
│   └── api/
│       └── openapi.yaml
└── [3] Configuration Examples (Reference)
    └── config-examples/
        ├── claude-desktop.json
        └── mcp-config.yaml
```

4. **Include summary statistics**:

```
## Summary
- Total documents: X
- Categories: [list of unique categories]
- Tags: [list of unique tags with counts]
- Missing frontmatter: X files
```

5. **Highlight issues** (if any):
   - Files without frontmatter
   - Duplicate order numbers in same directory
   - Orphan documents (no parent)

## Output Format

```markdown
# Documentation Structure

## docs/

### guides/ (Guides)
| Order | File | Title | Tags |
|-------|------|-------|------|
| 1 | getting-started.md | Getting Started | beginner, setup |
| 2 | configuration.md | Configuration Guide | config |

### guides/security/ (Security)
| Order | File | Title | Tags |
|-------|------|-------|------|
| 1 | authentication.md | Authentication Guide | security, auth |

## Statistics

- **Total Files**: 15
- **Categories**: Guides (8), API (4), Reference (3)
- **Most Used Tags**: security (5), api (4), beginner (3)

## Issues Found

- `docs/api/endpoints.md` - Missing frontmatter
- `docs/guides/` - Duplicate order 2: setup.md, config.md
```

## Example Usage

```
/doc-preview                    # Preview all documentation
/doc-preview docs/guides/       # Preview guides only
/doc-preview example/           # Preview example docs
```
