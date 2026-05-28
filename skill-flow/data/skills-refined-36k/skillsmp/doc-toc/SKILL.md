---
name: doc-toc
description: Generate or update table of contents for a documentation file. Creates markdown TOC from headers. Use after adding sections or to standardize existing docs.
argument-hint: <file-path>
allowed-tools: Read, Edit
---

# Generate Table of Contents

Generate or update a markdown table of contents for a documentation file.

## Instructions

1. **Read the target file**

2. **Extract all headers** (H2 and H3 only):
   - Skip H1 (document title)
   - Skip H4+ (too detailed for TOC)

3. **Generate anchor links**:
   - Convert header text to lowercase
   - Replace spaces with hyphens
   - Remove special characters
   - Example: `## Getting Started` -> `#getting-started`

4. **Format the TOC**:

```markdown
## Table of Contents

1. [Section One](#section-one)
2. [Section Two](#section-two)
   - [Subsection A](#subsection-a)
   - [Subsection B](#subsection-b)
3. [Section Three](#section-three)
```

5. **Insert or replace**:
   - If `## Table of Contents` exists, replace its contents
   - Otherwise, insert after the introduction paragraph (first paragraph after H1)

## TOC Rules

- Include H2 headers as numbered items
- Include H3 headers as sub-bullets under their parent H2
- Do not include H4+ headers
- Do not include "Table of Contents" itself
- Skip special sections: "Related Resources", "See Also", "References"

## Example

**Input file:**
```markdown
# My Guide

This guide explains something important.

## Prerequisites

Content...

## Installation

Content...

### Using pip

Content...

### Using conda

Content...

## Configuration

Content...

## Related Resources

Links...
```

**Generated TOC:**
```markdown
## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
   - [Using pip](#using-pip)
   - [Using conda](#using-conda)
3. [Configuration](#configuration)
```

## Example Usage

```
/doc-toc docs/guides/getting-started.md
/doc-toc example/api/authentication.md
```
