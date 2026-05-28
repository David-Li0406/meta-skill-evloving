---
name: check-docs
description: Verify documentation quality - checks README.md, CLAUDE.md, and other docs for completeness and accuracy
allowed-tools: Bash, Read, Glob, Grep
---

# Check Docs Skill

Verify that project documentation is complete, accurate, and up-to-date.

## Usage

```bash
/check-docs           # Check docs in current directory
/check-docs ./path    # Check docs in specific path
```

## What Gets Checked

| File | Checks |
|------|--------|
| README.md | Exists, non-empty, links valid, install steps current |
| CLAUDE.md | Exists (if Claude project), paths valid, commands work |
| Other .md | Exist if referenced, links valid |

## Output

Checklist format showing pass/fail for each check with details on issues found.

## Runbook

Full procedure: `runbook/check-docs.md` in your knowledge base.
