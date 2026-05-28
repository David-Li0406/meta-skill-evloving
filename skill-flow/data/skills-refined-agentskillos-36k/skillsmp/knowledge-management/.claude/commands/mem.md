---
description: Quick knowledge capture during work sessions
---

# Memory - Quick Knowledge Capture

จับความรู้แบบรวดเร็วระหว่างทำงาน (Layer 1)

## Usage

```
/mem [descriptive title]
```

**Output:** `$PROJECT_ROOT/docs/learnings/YYYY-MM/DD/HH.MM_[slug].md`

## Instructions

1. **Process title** → slug (lowercase, hyphens)
2. **Gather context**: timestamp, branch, recent commits
3. **Create directory**: `docs/learnings/YYYY-MM/DD/`
4. **Generate file** with template below
5. **Commit**: `git commit -m "learn: [title]"`

## Template

```markdown
# [Title]

| Field | Value |
|-------|-------|
| **Captured** | YYYY-MM-DD HH:MM (Asia/Bangkok) |
| **Branch** | current-branch |
| **Context** | what were you working on |

---

## Key Insight

> One-sentence summary

## What We Learned

- Discovery 1
- Discovery 2

## Gotchas & Warnings

- Pitfall to avoid

## Related

- Commits: `abc1234`
- Files: `path/to/file.go`

## Tags

`tag1` `tag2`
```

## Rules

| Rule | Description |
|------|-------------|
| **FAST** | Complete in < 20 seconds |
| **KNOWLEDGE-FOCUSED** | Insights, not task logs |
| **SEARCHABLE** | Clear titles and tags |
