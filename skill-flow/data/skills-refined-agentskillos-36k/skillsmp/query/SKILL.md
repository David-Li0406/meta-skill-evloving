---
name: query
description: Query data from this vault. USE WHEN user asks about projects, clients, tasks, daily notes. Use grep to extract frontmatter - do NOT read full files.
---

# Query Skill

## IMPORTANT

**Use `grep` to extract frontmatter. Do NOT read full files.**

## Projects

```bash
grep -h "^status:\|^priority:\|^deadline:" Projects/*.md
```

Or per-file with filename:
```bash
grep -l "" Projects/*.md | while read f; do
  echo "=== $(basename "$f" .md) ==="
  grep "^status:\|^priority:\|^deadline:" "$f"
done
```

**Present as table:**
| Project | Status | Priority | Deadline |
|---------|--------|----------|----------|

## Clients

```bash
grep -l "" Clients/*.md | while read f; do
  echo "=== $(basename "$f" .md) ==="
  grep "^stage:\|^company:\|^next_action:" "$f"
done
```

**Present as table:**
| Client | Company | Stage | Next Action |
|--------|---------|-------|-------------|

## Tasks

```bash
curl -s "http://127.0.0.1:8090/api/tasks"
```

## Daily Notes

```bash
ls -t Daily/*.md | head -5 | while read f; do
  echo "=== $(basename "$f" .md) ==="
  grep "^mood:\|^energy:\|^sleep_quality:" "$f"
done
```

## Output

Always present results as markdown table.
