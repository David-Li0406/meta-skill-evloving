---
name: skill-evolution-manager
description: Use this skill when you want to extract and store user experiences, best practices, and solutions during conversations, ensuring they are preserved and accessible for future use.
---

# Skill Evolution Manager

The central hub for managing skill evolution, responsible for extracting and persisting user experiences and best practices.

## Core Responsibilities

1. **Experience Extraction**: Convert user feedback into structured data.
2. **Incremental Storage**: Store experiences categorized by technology stack and context.
3. **On-Demand Loading**: Load relevant experiences only when needed.

## Trigger Conditions

- `/evolve`
- "记住这个" (Remember this)
- "保存经验" (Save experience)
- "复盘" (Review)
- "记录这次的教训" (Record this lesson)

## Workflow

### Step 1: Experience Extraction

Scan the context → Identify experience types → Categorize and store.

### Step 2: Storage Commands

```bash
# Store preferences
python scripts/store_experience.py --preference "preference"

# Store fixes
python scripts/store_experience.py --fix "fix"

# Store technology patterns
python scripts/store_experience.py --tech <tech> --pattern "pattern"

# Store context triggers
python scripts/store_experience.py --context <ctx> --instruction "instruction"
```

### Step 3: Query Commands

```bash
python scripts/query_experience.py --tech react
python scripts/query_experience.py --context when_testing
python scripts/query_experience.py --search "keyword"
```

## Storage Structure

```
experience/
├── index.json       # Index summary
├── tech/            # Categorized by technology stack
│   ├── react.json
│   └── python.json
└── contexts/        # Categorized by context
    └── when_testing.json
```

## Scripts

| Script | Purpose |
|--------|---------|
| `merge_evolution.py` | Merge old format data |
| `smart_stitch.py` | Migrate to incremental structure |
| `trigger_detector.py` | Detect evolution trigger conditions |
| `align_all.py` | Batch align all skills |

## Unified Knowledge Base Integration

### Sync to Unified Knowledge Base on Evolution

When an evolution trigger is detected, in addition to updating local experience storage, sync to the unified knowledge base:

```bash
# Analyze session content and store in the unified knowledge base
cat session_content.txt | python knowledge-base/scripts/knowledge_summarizer.py \
  --auto-store \
  --session-id "{session_id}"
```

### Knowledge Classification Mapping

| Local Experience Type | Unified Knowledge Base Classification |
|-----------------------|--------------------------------------|
| preference            | experience                           |
| fix                   | problem                              |
| tech pattern          | tech-stack                           |
| context trigger       | scenario                             |

### Workflow

```
Evolution Trigger
    │
    ├── Local Storage (experience/)
    │
    └── Sync to Unified Knowledge Base (knowledge-base/)
        │
        ├── Auto-classification
        ├── Generate Trigger Keywords
        └── Update Index
```