---
name: doc-lint
description: Quick lint check for a single documentation file. Faster than full validation - checks frontmatter and basic formatting only. Use during writing to catch issues early.
argument-hint: <file-path>
allowed-tools: Read
---

# Quick Documentation Lint

Perform a fast lint check on a single documentation file.

## Instructions

1. **Read the specified file** using the Read tool

2. **Check frontmatter** (first priority):

```
Required fields:
- title: string (non-empty)
- category: string (non-empty)
- tags: array (at least one tag)
- order: integer (>= 0)
```

3. **Check markdown basics**:
   - Exactly one H1 header
   - H1 appears before any other content (after frontmatter)
   - No skipped header levels
   - Code blocks have language tags

4. **Check line length**:
   - Flag lines > 100 characters
   - Ignore: URLs, code blocks, tables

5. **Check naming**:
   - Filename should be kebab-case
   - No uppercase letters
   - No underscores

## Output Format

Use a compact, scannable format:

```
## Lint: docs/guides/my-doc.md

[PASS] Frontmatter valid
[PASS] Single H1 header
[FAIL] Line 23: exceeds 100 chars (142)
[FAIL] Line 45: code block missing language
[WARN] Line 67: H4 after H2 (skipped H3)

Result: 2 errors, 1 warning
```

Or for passing files:

```
## Lint: docs/guides/my-doc.md

All checks passed!
```

## Checks Performed

| Check | Severity | Description |
|-------|----------|-------------|
| Frontmatter exists | ERROR | Must have YAML frontmatter |
| Required fields | ERROR | title, category, tags, order |
| Single H1 | ERROR | Exactly one # header |
| Header hierarchy | WARN | No skipped levels |
| Code language | ERROR | All ``` blocks need language |
| Line length | WARN | Lines > 100 chars |
| Filename format | WARN | Must be kebab-case |

## Example Usage

```
/doc-lint docs/guides/getting-started.md
/doc-lint example/api/authentication.md
```
