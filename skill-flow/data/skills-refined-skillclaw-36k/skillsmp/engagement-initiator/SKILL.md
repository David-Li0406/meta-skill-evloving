---
name: engagement-initiator
description: Creates customer engagement folders with task timelines, metadata, and knowledge graph entries. Use when starting new engagements, creating engagement structures, or when user mentions customer names with dates, CEHub links, qualification notes, or says "create engagement" or "new engagement".
---

# Engagement Initiator

Creates engagement folder structure in OneDrive with tasks, metadata, and knowledge graph entries.

## Quick Start

**Minimal**:
```
"Create engagement for [Customer] on [Date]"
```

**With context**:
```
"[Customer] [Date], CEHub: [url]"
"[Customer] [Date], qualification notes: [paste]"
```

## Output Structure

```
C:\Users\brecol\OneDrive - Microsoft\Engagements\[Customer]-[Date]/
├── tasks.csv (ready for Planner import)
├── engagement_metadata.json
├── README.md
└── [additional files based on input]
```

## Configuration

**Configuration File**: `config.json` (root of workspace)

```json
{
  "engagements_base_path": "C:\\Users\\<username>\\OneDrive - Microsoft\\Engagements"
}
```

1. Copy `config.example.json` to `config.json`
2. Update `engagements_base_path` with your OneDrive path
3. `config.json` is gitignored and won't be committed

All engagements are created in the configured OneDrive location.

## Workflow Checklist

```
- [ ] Extract customer name and date
- [ ] Calculate timeline position
- [ ] Create folder: C:\Users\brecol\OneDrive - Microsoft\Engagements\[Customer]-[Date]/
- [ ] Generate tasks via business_days.py
- [ ] Create metadata file
- [ ] Store in knowledge graph
- [ ] Display status
```

### Timeline Status

Show current position:
```
📊 T-15 (Final prep)

OVERDUE:
❗ T-28: Schedule Internal Precall

DUE THIS WEEK:
📅 T-14: Execute Customer Precall
```

## Scripts

**scripts/business_days.py**: Generates task timeline

```bash
python scripts/business_days.py "[Customer]" "YYYY-MM-DD"
```

Outputs tasks.csv with 15 tasks (T-28 to T+3).

## Knowledge Graph

Create entities:
```python
memory:create_entities([{
    "name": customer_name,
    "entityType": "Customer",
    "observations": [industry, customer_type, context]
}])

memory:create_entities([{
    "name": f"{customer_name} Engagement - {date}",
    "entityType": "Engagement", 
    "observations": [date, type, status, timeline_position]
}])

memory:create_relations([{
    "from": engagement_name,
    "to": customer_name,
    "relationType": "conducted_for"
}])
```

## Metadata Schema

```json
{
  "customer": "string",
  "engagement_date": "YYYY-MM-DD",
  "timeline_position": "T-X or T+X",
  "status": "planned|active|past",
  "cehub_link": "string|null",
  "tasks_generated": true
}
```

## Next Steps

- **agenda-builder**: Build engagement agenda
- **cehub-integration**: Add qualification notes

## Reference

See [references/implementation.md](references/implementation.md) for technical details.
