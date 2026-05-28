# CSV Reference for Agents

This document provides efficient patterns for querying backlog data with minimal token usage.

---

## File Locations

```
.claude/plans/backlog/data/backlog.csv   # Main table (280 items)
.claude/plans/backlog/data/sprints.csv   # Sprint history (35 sprints)
.claude/plans/backlog/data/changelog.csv # Audit trail (153 entries)
```

---

## Python Patterns (Preferred)

### Load and Filter

```python
import csv

def load_backlog():
    with open('.claude/plans/backlog/data/backlog.csv') as f:
        return list(csv.DictReader(f))

# Get all pending items
pending = [i for i in load_backlog() if i['status'].lower() == 'pending']

# Get high priority pending
high_pending = [
    i for i in load_backlog()
    if i['status'].lower() == 'pending'
    and i['priority'].lower() == 'high'
]

# Search by title
def search(query):
    q = query.lower()
    return [i for i in load_backlog() if q in i['title'].lower()]
```

### Count by Category

```python
from collections import Counter

items = load_backlog()
by_status = Counter(i['status'].lower() for i in items)
# {'pending': 176, 'completed': 97, ...}
```

### Sprint Items

```python
def get_sprint_items(sprint_id):
    return [
        i for i in load_backlog()
        if i['sprint'].upper() == sprint_id.upper()
    ]

sprint_42 = get_sprint_items('SPRINT-042')
```

---

## Bash Patterns (Quick Lookups)

### Basic Queries

```bash
# Count items by status
cut -d',' -f5 .claude/plans/backlog/data/backlog.csv | sort | uniq -c

# Find all pending high priority
grep ",high,pending," .claude/plans/backlog/data/backlog.csv

# Search titles
grep -i "sync" .claude/plans/backlog/data/backlog.csv

# Get sprint items
grep ",SPRINT-042," .claude/plans/backlog/data/backlog.csv
```

### Using the Query Script

```bash
# More reliable than grep for complex queries
python .claude/plans/backlog/scripts/queries.py status pending
python .claude/plans/backlog/scripts/queries.py priority high --status pending
python .claude/plans/backlog/scripts/queries.py search "message"
python .claude/plans/backlog/scripts/queries.py stats
```

---

## CSV Schema Quick Reference

### backlog.csv Columns

| # | Column | Description |
|---|--------|-------------|
| 1 | id | BACKLOG-XXX |
| 2 | title | Brief description |
| 3 | category | bug/feature/enhancement/refactor/... |
| 4 | priority | critical/high/medium/low |
| 5 | status | pending/in-progress/completed/... |
| 6 | sprint | SPRINT-XXX or - |
| 7 | est_tokens | ~30K or - |
| 8 | actual_tokens | 28K or - |
| 9 | variance | -7% or - |
| 10 | file | [BACKLOG-XXX.md] |

### sprints.csv Columns

| # | Column | Description |
|---|--------|-------------|
| 1 | sprint_id | SPRINT-XXX |
| 2 | name | Sprint name |
| 3 | status | planning/active/completed/deprecated |
| 4 | items_completed | Summary of completed items |

---

## Token Efficiency Tips

1. **Use Python over bash** - CSV module handles quoting/escaping correctly
2. **Filter early** - Don't load all items then filter in memory
3. **Query script first** - Use queries.py before writing custom code
4. **Avoid reading INDEX-archive.md** - It's 25K+ tokens; use CSVs instead (~500 tokens per query)

---

## Modifying Data

### Add Row

```python
import csv

new_item = {
    'id': 'BACKLOG-303',
    'title': 'New Feature',
    'category': 'feature',
    'priority': 'medium',
    'status': 'pending',
    'sprint': '-',
    'est_tokens': '~20K',
    'actual_tokens': '-',
    'variance': '-',
    'file': '[BACKLOG-303.md]'
}

with open('.claude/plans/backlog/data/backlog.csv', 'a', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=new_item.keys())
    writer.writerow(new_item)
```

### Update Row

```python
import csv

def update_status(item_id, new_status):
    with open('.claude/plans/backlog/data/backlog.csv') as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        if row['id'] == item_id:
            row['status'] = new_status

    with open('.claude/plans/backlog/data/backlog.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

update_status('BACKLOG-220', 'completed')
```

### Always Validate After Changes

```bash
python .claude/plans/backlog/scripts/validate.py
```
