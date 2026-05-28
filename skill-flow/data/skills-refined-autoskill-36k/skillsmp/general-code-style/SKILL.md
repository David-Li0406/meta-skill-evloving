---
name: general-code-style
description: Language-agnostic code style conventions. Use when writing code in any language, writing or editing Markdown documents, or defining constants.
---

# General Code Style

## Regular Expression Constants

Use the suffix `_RE` for regular expression constants:

- Preferred: `MAILTO_RE`, `URL_RE`, `EMAIL_RE`
- Avoid: `MAILTO_REGEX`, `URL_REGEX`, `EMAIL_REGEX`

## Markdown Formatting

Use one sentence per line in Markdown documents.

**Benefits:**

- Cleaner diffs
- Easier line-by-line editing
- Better version control history

**Example:**

```markdown
This is the first sentence.
This is the second sentence.
This is the third sentence.
```

**Not:**

```markdown
This is the first sentence. This is the second sentence. This is the third sentence.
```
