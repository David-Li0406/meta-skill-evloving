---
name: doc-create
description: Create a new documentation file with proper YAML frontmatter and structure following project standards. Use when creating new guides, API docs, tutorials, or reference pages.
argument-hint: <path> [--type guide|api|tutorial|reference]
allowed-tools: Read, Write, Glob
---

# Create Documentation File

Create a new documentation file following the project's documentation standards.

## Instructions

When creating a new documentation file:

1. **Parse the arguments** to determine:
   - Target path (required) - where to create the file
   - Document type (optional) - guide, api, tutorial, or reference

2. **Validate the path**:
   - Must use kebab-case for filename (e.g., `getting-started.md`)
   - Must be in a valid docs directory (`docs/` or `example/`)
   - Directory must use lowercase with hyphens

3. **Generate proper YAML frontmatter** with ALL required fields:

```yaml
---
title: "Document Title"           # Human-readable, derived from filename
category: "Category Name"         # Based on parent directory or type
tags: ["tag1", "tag2", "tag3"]   # Relevant searchable tags
order: 1                          # Position in hierarchy (check siblings)
---
```

4. **Include standard structure** based on document type:

**For Guides/Tutorials:**
```markdown
# Title

Brief introduction (2-3 sentences) explaining what this document covers.

## Prerequisites

- Requirement 1
- Requirement 2

## Section 1

Content...

## Section 2

Content...

## Related Resources

- [Related Doc](./related-doc.md)
```

**For API Documentation:**
```markdown
# Function/Tool Name

Brief description of what it does.

## Signature

\`\`\`python
def function_name(param: type) -> ReturnType:
\`\`\`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `param` | type | Yes/No | Description |

## Returns

Description of return value.

## Example

\`\`\`python
# Example usage
result = function_name(value)
\`\`\`
```

**For Reference:**
```markdown
# Reference Title

Overview of this reference section.

## Table of Contents

1. [Section 1](#section-1)
2. [Section 2](#section-2)

## Section 1

Content...

## Section 2

Content...
```

5. **Determine the order field**:
   - Read existing files in the same directory
   - Set order to next available number (0-based)

6. **Write the file** with the generated content

## Validation Checklist

Before writing, verify:
- [ ] Filename is kebab-case
- [ ] All required frontmatter fields present
- [ ] Title uses title case
- [ ] Category matches directory structure
- [ ] Tags are relevant and lowercase
- [ ] H1 matches the title field
- [ ] Line length under 100 characters
- [ ] Code blocks have language specified

## Example Usage

```
/doc-create docs/guides/deployment.md --type guide
/doc-create docs/api/search-tool.md --type api
/doc-create example/reference/cli-options.md --type reference
```
