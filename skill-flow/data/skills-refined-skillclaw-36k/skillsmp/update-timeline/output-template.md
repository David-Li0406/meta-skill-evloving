# Output Template

## File Header

```yaml
---
title: Project - Chronological Events Index
created: YYYY-MM-DD
updated: YYYY-MM-DD
date_range: [earliest] to [latest]
sources:
  hyprnote_transcripts: N
  notion_transcripts: N
  whatsapp_clusters: N
  hailer_clusters: N
total_entries: N
description: Chronological organization of all project communications with deep analysis
---
```

## Entry Format

### For Transcripts (Hyprnote/Notion)

```markdown
### YYYY-MM-DD | [Source] - [Descriptive Title]

**Type:** Meeting transcript
**File:** `path/to/file`
**Participants:** Name (role), Name (role)
**Relevance:** High/Medium/Low

**Summary:**
[2-4 sentence substantive summary of what was discussed and concluded]

**Key Points:**
- [Decision/insight/action item]
- [Decision/insight/action item]

**Notes from memo:** *(if _memo.md exists)*
- [Key point from human notes]

---
```

### For Chat Clusters (WhatsApp/Hailer)

```markdown
### YYYY-MM-DD to YYYY-MM-DD | [Source] - [Topic Title]

**Type:** Chat cluster
**File:** `path/to/file`
**Participants:** Name, Name, Name
**Relevance:** High/Medium/Low

**Summary:**
[2-4 sentences summarizing this conversation cluster]

**Key Events:**
- [Date]: [What happened]
- [Date]: [What happened]

**Decisions/Outcomes:**
- [Decision made]

**Attachments:**
| File | Description |
|------|-------------|
| `filename.jpg` | [Detailed description of image content] |
| `document.pdf` | [Summary of document purpose and key content] |

---
```

## Entry Ordering

1. Sort ALL entries by date (newest first in processing, but output oldest-first)
2. Group by month in output
3. Within same date: order by timestamp
4. WhatsApp/Hailer clusters: position by START date of cluster
