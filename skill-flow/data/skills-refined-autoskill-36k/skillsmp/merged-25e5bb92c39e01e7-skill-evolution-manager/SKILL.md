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

### Step 4: Generate Structured JSON

Convert extracted experiences into JSON format:

```json
{
  "preferences": ["<user preference>"],
  "fixes": ["<known fix>"],
  "contexts": ["<context note>"],
  "custom_prompts": "<custom instruction>"
}
```

### Step 5: Incremental Merging

Run the following command to merge experiences into `evolution.json`:

```bash
python scripts/merge_evolution.py <skill_dir> '<json_string>'
```

### Step 6: Smart Stitching

Automatically write experiences into `SKILL.md`:

```bash
python scripts/smart_stitch.py <skill_dir>
```

Generated section in `SKILL.md`:

```markdown
## User-Learned Best Practices & Constraints

> **Auto-Generated Section**: This section is automatically maintained by skill-evolution; do not edit manually.

### User Preferences
- User preference 1
- User preference 2

### Known Fixes & Workarounds
- Fix solution 1
- Fix solution 2

### Context-Specific Notes
- Context note 1
- Context note 2

### Custom Instruction Injection
Custom instruction content...
```

### Step 7: Cross-Version Alignment

After a skill update, run the following command to restore experiences:

```bash
python scripts/align_all.py <skills_dir>
```

## Storage Structure

```
experience/
├── evolution.json    # Stores user experiences
└── contexts/         # Categorized by context
```

## Best Practices

1. **Modify via evolution.json**: Do not edit the experience sections in `SKILL.md` directly; all modifications should be made through `evolution.json`.
2. **Regular Reviews**: Record experiences and insights promptly after encountering issues or discovering tips.
3. **Align After Updates**: Run alignment scripts after any skill updates to ensure experiences are preserved.
4. **Backup Important Data**: Use backup options to protect critical experience data.

## Example Scenarios

### Example 1: Record User Preference

```
User: 记录一下，我希望下载视频时默认不带字幕 (Record that I want videos to download without subtitles by default)

Agent:
1. Identify this as a user preference.
2. Generate JSON: {"preferences": ["下载视频时默认不带字幕"]}.
3. Run merge_evolution.py to merge into evolution.json.
4. Run smart_stitch.py to update SKILL.md.
```

### Example 2: Record Fix Solution

```
User: 刚才那个路径问题，记住 Windows 下要用双反斜杠 (Remember that for the path issue, I need to use double backslashes on Windows)

Agent:
1. Identify this as a fix solution.
2. Generate JSON: {"fixes": ["Windows 下路径使用双反斜杠转义"]}.
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

- **skill-factory**: Automatically enable evolution for created Skills (`evolution_enabled: true`).
- **skill-manager**: Call align_all.py after updating Skills to restore experiences.
- **skill-creator**: Follow the same experience section format for consistency.