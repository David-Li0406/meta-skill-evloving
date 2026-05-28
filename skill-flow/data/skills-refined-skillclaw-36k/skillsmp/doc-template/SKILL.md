---
name: doc-template
description: Generate documentation templates for common document types. Outputs a ready-to-fill template with proper frontmatter and structure. Use when starting a new document.
argument-hint: <type> [title]
allowed-tools: Read
---

# Generate Documentation Template

Generate a documentation template for common document types.

## Instructions

1. **Parse arguments**:
   - `type`: guide, api, tutorial, reference, changelog, troubleshooting
   - `title` (optional): Title for the document

2. **Generate the appropriate template**:

### Guide Template (`guide`)

```markdown
---
title: "${TITLE}"
category: "Guides"
tags: ["guide"]
order: 1
---

# ${TITLE}

Brief introduction explaining what this guide covers and who should read it.

## Prerequisites

Before you begin, ensure you have:

- Prerequisite 1
- Prerequisite 2

## Overview

High-level explanation of the topic.

## Step 1: First Step

Detailed instructions for the first step.

\`\`\`bash
$ example command
\`\`\`

## Step 2: Second Step

Detailed instructions for the second step.

## Verification

How to verify the setup/configuration is working.

## Troubleshooting

Common issues and their solutions.

## Next Steps

- [Related Guide 1](./related-guide-1.md)
- [Related Guide 2](./related-guide-2.md)
```

### API Template (`api`)

```markdown
---
title: "${TITLE}"
category: "API Reference"
tags: ["api"]
order: 1
---

# ${TITLE}

Brief description of what this API/tool does.

## Signature

\`\`\`python
def function_name(
    required_param: str,
    optional_param: Optional[str] = None
) -> ReturnType:
    """Function description."""
\`\`\`

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `required_param` | `str` | Yes | - | Description |
| `optional_param` | `str` | No | `None` | Description |

## Returns

`ReturnType` - Description of what is returned.

## Raises

| Exception | Condition |
|-----------|-----------|
| `ValueError` | When input is invalid |
| `FileNotFoundError` | When file doesn't exist |

## Examples

### Basic Usage

\`\`\`python
result = function_name("value")
print(result)
\`\`\`

### Advanced Usage

\`\`\`python
result = function_name(
    required_param="value",
    optional_param="option"
)
\`\`\`

## Related

- [Related API 1](./related-api-1.md)
- [Related API 2](./related-api-2.md)
```

### Tutorial Template (`tutorial`)

```markdown
---
title: "${TITLE}"
category: "Tutorials"
tags: ["tutorial", "beginner"]
order: 1
---

# ${TITLE}

In this tutorial, you'll learn how to [main objective]. By the end, you'll be
able to [specific outcome].

## What You'll Build

Brief description of the end result with screenshot or diagram if applicable.

## Prerequisites

- Prerequisite 1
- Prerequisite 2
- Time required: ~X minutes

## Step 1: Setup

First, we'll set up the project structure.

\`\`\`bash
$ mkdir my-project
$ cd my-project
\`\`\`

## Step 2: Implementation

Now let's implement the main functionality.

\`\`\`python
# Your code here
\`\`\`

## Step 3: Testing

Let's verify everything works correctly.

\`\`\`bash
$ python test.py
Expected output here
\`\`\`

## Summary

In this tutorial, you learned how to:

- Point 1
- Point 2
- Point 3

## Next Steps

- [Advanced Tutorial](./advanced-tutorial.md)
- [Related Concept](./related-concept.md)
```

### Reference Template (`reference`)

```markdown
---
title: "${TITLE}"
category: "Reference"
tags: ["reference"]
order: 1
---

# ${TITLE}

Comprehensive reference for [topic].

## Table of Contents

1. [Section 1](#section-1)
2. [Section 2](#section-2)
3. [Section 3](#section-3)

## Section 1

### Subsection 1.1

Content...

### Subsection 1.2

Content...

## Section 2

### Subsection 2.1

Content...

## Section 3

Content...

## See Also

- [Related Reference 1](./related-1.md)
- [Related Reference 2](./related-2.md)
```

### Troubleshooting Template (`troubleshooting`)

```markdown
---
title: "${TITLE}"
category: "Troubleshooting"
tags: ["troubleshooting", "debugging"]
order: 1
---

# ${TITLE}

Solutions to common problems with [feature/component].

## Quick Diagnostics

Run these commands to gather diagnostic information:

\`\`\`bash
$ diagnostic-command-1
$ diagnostic-command-2
\`\`\`

## Common Issues

### Issue: Error message or symptom

**Symptoms:**
- What the user sees
- Error messages

**Cause:**
Why this happens.

**Solution:**

1. First step
2. Second step

\`\`\`bash
$ fix-command
\`\`\`

### Issue: Another common problem

**Symptoms:**
- Symptom description

**Cause:**
Root cause explanation.

**Solution:**

Step-by-step fix instructions.

## Getting Help

If your issue isn't listed here:

1. Check the [FAQ](./faq.md)
2. Search [existing issues](https://github.com/repo/issues)
3. Open a new issue with diagnostic output
```

## Example Usage

```
/doc-template guide                     # Basic guide template
/doc-template api "search_documents"    # API template with title
/doc-template tutorial "Build a CLI"    # Tutorial with title
/doc-template troubleshooting           # Troubleshooting template
```
