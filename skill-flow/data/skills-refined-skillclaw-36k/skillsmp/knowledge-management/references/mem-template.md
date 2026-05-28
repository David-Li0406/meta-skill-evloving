# /mem Template

## File Path

```
docs/learnings/YYYY-MM/DD/HH.MM_[slug].md
```

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

> One-sentence summary of what you learned

## What We Learned

- Discovery 1
- Discovery 2

## How Things Connect

- Component A → relates to → Component B
- Pattern X → enables → Feature Y

## Gotchas & Warnings

- Pitfall to avoid
- Edge case discovered

## Related

- Commits: `abc1234`, `def5678`
- Files: `path/to/file.go`
- Issue: #number (if applicable)

## Tags

`tag1` `tag2` `tag3`

---

## Raw Thoughts

<!-- Unprocessed ideas for later -->
```

## Gather Context

```bash
# Timestamp
TZ='Asia/Bangkok' date '+%Y-%m-%d %H:%M:%S'

# Recent commits
git log --oneline -5

# Current branch
git branch --show-current

# Create directory
mkdir -p docs/learnings/$(TZ='Asia/Bangkok' date '+%Y-%m')/$(TZ='Asia/Bangkok' date '+%d')
```

## Commit

```bash
git add docs/learnings/
git commit -m "learn: [title]"
```
