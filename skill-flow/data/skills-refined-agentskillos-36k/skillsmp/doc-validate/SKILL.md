---
name: doc-validate
description: Validate documentation files against project standards. Checks frontmatter, markdown formatting, links, and content structure. Use to verify docs before committing or to audit existing documentation.
argument-hint: [path] [--fix]
allowed-tools: Read, Bash, Glob, Grep, Edit
---

# Validate Documentation

Validate documentation files against the project's documentation standards.

## Instructions

1. **Determine scope**:
   - If a specific path is given, validate that file/directory
   - If no path given, validate all docs in `docs/` and `example/`

2. **Run the validation script** if available:

```bash
python scripts/validate_docs.py $ARGUMENTS
```

3. **If script unavailable, perform manual checks**:

### Frontmatter Validation (Critical)

Check each markdown file for:
- [ ] YAML frontmatter exists (between `---` markers)
- [ ] `title` field present and is a string
- [ ] `category` field present and is a string
- [ ] `tags` field present and is an array
- [ ] `order` field present and is an integer

### Markdown Formatting (Critical)

- [ ] Only one H1 (`#`) per document
- [ ] No skipped header levels (H1 -> H3 without H2)
- [ ] All code blocks have language specified
- [ ] Line length under 100 characters (except URLs, code, tables)

### Content Structure (Warning)

- [ ] H1 matches the `title` frontmatter field
- [ ] Introduction present after H1
- [ ] Table of contents for docs with >3 sections
- [ ] Related resources section at end

### Links (Critical)

- [ ] Internal links use relative paths with `.md` extension
- [ ] Internal links resolve to existing files
- [ ] No "click here" link text

## Output Format

Report findings in this format:

```
## Validation Results

### file-path.md
- [CRITICAL] Missing required frontmatter field: tags
- [WARNING] Line 45 exceeds 100 characters
- [INFO] Consider adding table of contents

### Summary
- Files checked: X
- Critical issues: X
- Warnings: X
- Passed: X
```

## Severity Levels

| Level | Action Required | Examples |
|-------|----------------|----------|
| CRITICAL | Must fix before commit | Missing frontmatter, broken links, no H1 |
| WARNING | Should fix | Long lines, missing TOC |
| INFO | Optional | Unusual categories, style suggestions |

## Auto-Fix Mode

If `--fix` is specified, automatically fix:
- Missing language tags on code blocks (add `text`)
- Trailing whitespace
- Missing blank lines around lists
- Inconsistent list markers (convert to `-`)

Do NOT auto-fix:
- Missing frontmatter fields (requires human input)
- Broken links
- Content structure issues

## Example Usage

```
/doc-validate                           # Validate all docs
/doc-validate docs/guides/              # Validate guides directory
/doc-validate docs/api/search.md        # Validate single file
/doc-validate docs/ --fix               # Validate and auto-fix
```
