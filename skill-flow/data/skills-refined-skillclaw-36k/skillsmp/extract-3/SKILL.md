---
name: extract
description: 'Extract decisions and learnings from Claude session transcripts. Triggers: "extract learnings", "process pending", SessionStart hook.'
---

# Extract Skill

Process pending learning extractions from previous sessions.

## How It Works

This skill closes the knowledge loop by processing sessions queued for learning extraction.

```
Session N ends:
  → ao forge --last-session --queue
  → Session queued in .agents/ao/pending.jsonl

Session N+1 starts:
  → ao extract (this skill)
  → Outputs extraction prompt
  → Claude extracts learnings
  → Writes to .agents/learnings/
  → Loop closed
```

## Triggers

- SessionStart hook (automatic)
- "extract learnings"
- "process pending"

## Usage

```bash
# Check for pending extractions and output prompt
ao extract

# Clear pending queue without processing
ao extract --clear

# Limit content size in prompt
ao extract --max-content 4000
```

## What It Outputs

When pending extractions exist, outputs a structured prompt:

```markdown
