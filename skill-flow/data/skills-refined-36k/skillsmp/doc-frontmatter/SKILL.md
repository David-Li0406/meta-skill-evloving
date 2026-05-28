---
name: doc-frontmatter
description: Add or fix YAML frontmatter for documentation files. Adds missing required fields or fixes invalid frontmatter. Use for bulk fixing or when validation fails.
argument-hint: <file-path> [--title "..."] [--category "..."] [--tags "..."]
allowed-tools: Read, Edit, Glob
---

# Fix Documentation Frontmatter

Add or repair YAML frontmatter for documentation files.

## Instructions

1. **Read the target file**

2. **Check current frontmatter status**:
   - No frontmatter: Generate complete frontmatter
   - Partial frontmatter: Add missing required fields
   - Invalid YAML: Fix syntax errors

3. **Required fields** (must all be present):

| Field | Type | How to determine value |
|-------|------|----------------------|
| `title` | string | From H1, or derive from filename |
| `category` | string | From parent directory name |
| `tags` | array | From content keywords |
| `order` | integer | Next available in directory |

4. **Derive values intelligently**:

**Title:**
- Use explicit `--title` if provided
- Otherwise extract from first H1 in document
- Otherwise derive from filename: `getting-started.md` -> `"Getting Started"`

**Category:**
- Use explicit `--category` if provided
- Otherwise derive from directory:
  - `docs/guides/` -> `"Guides"`
  - `docs/api/` -> `"API Reference"`
  - `docs/reference/` -> `"Reference"`
  - `example/tutorials/` -> `"Tutorials"`

**Tags:**
- Use explicit `--tags` if provided (comma-separated)
- Otherwise analyze content for keywords
- Always include category as a tag (lowercase)
- Suggest 2-4 relevant tags

**Order:**
- Check sibling files in same directory
- Find highest existing order number
- Set to next available (highest + 1)
- Default to 1 if first file

5. **Apply changes**:
   - If no frontmatter exists, add at top of file
   - If frontmatter exists, merge new fields (don't overwrite existing valid fields)

## Output Format

Show what was added/changed:

```
## Frontmatter Updated: docs/guides/new-doc.md

Added:
- title: "New Document"
- category: "Guides"
- tags: ["guide", "setup"]
- order: 3

Final frontmatter:
---
title: "New Document"
category: "Guides"
tags: ["guide", "setup"]
order: 3
---
```

## Batch Mode

If path is a directory, process all `.md` files:

```
/doc-frontmatter docs/guides/
```

Reports summary:
```
Processed 5 files:
- 2 files updated
- 1 file already valid
- 2 files created frontmatter
```

## Example Usage

```
/doc-frontmatter docs/new-doc.md                           # Auto-detect all
/doc-frontmatter docs/api/tool.md --category "API"         # Override category
/doc-frontmatter docs/guide.md --tags "beginner,setup"     # Specify tags
/doc-frontmatter docs/guides/                              # Batch process
```
