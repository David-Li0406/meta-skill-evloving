---
name: skill-evolution-manager
description: Use this skill to manage the evolution of user experiences and best practices during interactions, allowing for structured storage and retrieval of insights.
---

# Skill Evolution Manager

This skill serves as the central hub for managing the evolution of user experiences within the AI skill system. It supports the extraction, storage, and retrieval of insights based on user feedback.

## Core Responsibilities

1. **Experience Extraction**: Convert user feedback into structured data.
2. **Incremental Storage**: Store experiences categorized by technology stack and context.
3. **On-Demand Loading**: Load relevant experiences only when needed.

## Trigger Conditions

- `/evolve`
- "记住这个" (Remember this)
- "保存经验" (Save this experience)
- "复盘" (Review)
- "记录这次的教训" (Record this lesson)

## Workflow

### Step 1: Experience Extraction

Scan the context → Identify experience types → Categorize and store.

### Step 2: Storage Commands

```bash
# Store preferences
python scripts/store_experience.py --preference "<preference>"

# Store fix solutions
python scripts/store_experience.py --fix "<fix>"

# Store technology patterns
python scripts/store_experience.py --tech <tech> --pattern "<pattern>"

# Store context triggers
python scripts/store_experience.py --context <ctx> --instruction "<instruction>"
```

### Step 3: Query Commands

```bash
python scripts/query_experience.py --tech <tech>
python scripts/query_experience.py --context <ctx>
python scripts/query_experience.py --search "<keyword>"
```

## Storage Structure

```
experience/
├── index.json       # Index summary
├── tech/            # Categorized by technology stack
│   ├── <tech>.json
└── contexts/        # Categorized by context
    └── <context>.json
```

## Integration with Unified Knowledge Base

### Syncing to Unified Knowledge Base

When an evolution trigger is detected, sync to the unified knowledge base in addition to updating local experience storage:

```bash
# Analyze session content and store in the unified knowledge base
cat session_content.txt | python knowledge-base/scripts/knowledge_summarizer.py \
  --auto-store \
  --session-id "{session_id}"
```

### Knowledge Classification Mapping

| Local Experience Type | Unified Knowledge Base Category |
|-----------------------|--------------------------------|
| preference            | experience                     |
| fix                   | problem                        |
| tech pattern          | tech-stack                     |
| context trigger       | scenario                       |

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

## Best Practices

1. **Modify via evolution.json**: Do not directly edit the experience sections in SKILL.md; all modifications should be made through evolution.json.
2. **Regular Reviews**: Record experiences promptly whenever issues or tips arise during skill usage.
3. **Post-Update Alignment**: After any skill updates, run alignment scripts to restore experiences.
4. **Backup Important Experiences**: Use backup options to protect critical experience data.

## Example Scenarios

### Example 1: Record User Preference

```
User: 记录一下，我希望下载视频时默认不带字幕 (Record that I want videos to download without subtitles by default)

Agent:
1. Identify this as a user preference.
2. Generate JSON: {"preferences": ["下载视频时默认不带字幕"]}
3. Run merge_evolution.py to merge into evolution.json.
4. Run smart_stitch.py to update SKILL.md.
```

### Example 2: Record Fix Solution

```
User: 刚才那个路径问题，记住 Windows 下要用双反斜杠 (Remember that for the path issue, use double backslashes on Windows)

Agent:
1. Identify this as a fix solution.
2. Generate JSON: {"fixes": ["Windows 下路径使用双反斜杠转义"]}
3. Merge and stitch.
```

### Example 3: Batch Alignment

```
User: 我刚更新了几个 Skills，恢复一下经验 (I just updated several Skills, restore the experiences)

Agent:
1. Run align_all.py to scan all Skills.
2. Re-stitch experiences for each Skill with evolution.json.
3. Report alignment results.
```

## Collaboration with Other Skills

- **skill-factory**: Skills created automatically enable evolution (`evolution_enabled: true`).
- **skill-manager**: After updating Skills, call align_all.py to restore experiences.
- **skill-creator**: Follow the same experience section format for consistency.