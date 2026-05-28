---
name: julien-skill-move-to-core
description: "Add a skill to core sync config for global availability. Use when: move to core, add to sync, make skill global, sync skill."
license: Apache-2.0
metadata:
  author: "Julien"
  version: "1.0.0"
  category: "workflow"
triggers:
  - "move to core"
  - "add to core"
  - "add to sync"
  - "sync skill"
  - "make global"
  - "ajouter au core"
  - "synchroniser skill"
  - "rendre global"
---

# Move Skill to Core

Add a skill to `sync-config.json` to make it globally available across all projects.

## What is "Core"?

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-skill-move-to-core" activated
```

Core skills are:
- Synced to `~/.claude/skills/` via `/sync` command
- Available in ALL projects automatically
- Listed in `registry/sync-config.json`

## Process

### Step 1: Identify the skill

Ask user or detect from context:
- Skill name (e.g., `julien-calibre`)
- Or skill path (e.g., `skills/julien-calibre`)

### Step 2: Verify skill exists

```bash
# Check skill exists in marketplace
ls skills/<skill-name>/SKILL.md
```

If not found:
- Check if it's a local skill (`.claude/skills/`)
- Suggest using `julien-skill-migration` first

### Step 3: Check current sync-config

```bash
Read registry/sync-config.json
```

Verify skill is not already in `skills_to_sync`.

### Step 4: Add to sync-config.json

```bash
Edit registry/sync-config.json
# Add skill name to skills_to_sync array (alphabetically sorted by category)
```

**Sorting order:**
1. `julien-dev-*`
2. `julien-workflow-*`
3. `julien-ref-*`
4. `anthropic-*`
5. `julien-mcp-*`

### Step 5: Regenerate triggers

```bash
python scripts/generate-triggers.py
```

### Step 6: Confirm and suggest sync

```
Skill "<name>" ajouté au core.
Pour déployer: /sync
```

## Quick Command

```bash
# One-liner to add skill to core
python -c "
import json
skill = '<skill-name>'
with open('registry/sync-config.json', 'r+') as f:
    config = json.load(f)
    if skill not in config['skills_to_sync']:
        config['skills_to_sync'].append(skill)
        config['skills_to_sync'].sort()
        f.seek(0)
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.truncate()
        print(f'Added {skill} to core')
    else:
        print(f'{skill} already in core')
"
```

## Bulk Add

To add multiple skills at once:

```python
skills_to_add = [
    "julien-ref-ahk-v1",
    "julien-ref-ahk-v2",
    "julien-calibre"
]

# Add each to sync-config.json
```

## Show Current Core Skills

```bash
grep -A 50 '"skills_to_sync"' registry/sync-config.json | grep '"julien-' | wc -l
```

## Skill Chaining

### Skills Required Before
- Skill must exist in `skills/` directory
- If local skill: use `julien-skill-migration` first

### Input Expected
- Skill name to add to core

### Output Produced
- Updated `registry/sync-config.json`
- Regenerated `registry/skill-triggers.json`

### Compatible Skills After
- **/sync**: Deploy skills to `~/.claude/`

### Tools Used
- `Read`: Check sync-config.json
- `Edit`: Add skill to array
- `Bash`: Run generate-triggers.py

### Visual Workflow

```
User: "Add julien-calibre to core"
    ↓
[VERIFY] Skill exists in skills/?
    YES → Continue
    NO  → Suggest migration first
    ↓
[CHECK] Already in sync-config?
    YES → "Already in core"
    NO  → Continue
    ↓
[EDIT] Add to skills_to_sync
    ↓
[RUN] generate-triggers.py
    ↓
[DONE] "Run /sync to deploy"
```

## Usage Examples

**Single skill:**
```
User: "Move julien-calibre to core"
Claude: Adds to sync-config, regenerates triggers
Result: "julien-calibre ajouté. Run /sync"
```

**Multiple skills:**
```
User: "Add all julien-ref-* to core"
Claude: Finds matching skills, adds each
Result: "8 skills ajoutés. Run /sync"
```

**From local project:**
```
User: "Move my local skill to core"
Claude: "Use julien-skill-migration first to move to marketplace"
```
