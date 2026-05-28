---
name: memorybank-update
description: Comprehensive review and update of all Memory Bank files. Reads all 6 files, proposes targeted updates focusing on activeContext.md and progress.md, and validates results.
---

# Memory Bank: Update

Comprehensive review and update of entire Memory Bank.

**Helper Scripts Available:**
- `scripts/validate_memorybank.py` - Pre/post validation
- `scripts/detect_stale.py` - Find outdated info
- `scripts/extract_todos.py` - Extract action items

## Workflow

### 1. Announce
"Understood. Initiating a full Memory Bank review and update."

### 2. Validate
```bash
python scripts/validate_memorybank.py /path/to/project
```
Fix any errors before proceeding.

### 3. Detect Staleness
```bash
python scripts/detect_stale.py /path/to/project
```
Identify files needing attention.

### 4. Read All Files
Read in hierarchical order:
- projectbrief.md
- productContext.md, techContext.md, systemPatterns.md
- activeContext.md
- progress.md

### 5. Extract TODOs
```bash
python scripts/extract_todos.py /path/to/project
```
Get current action items.

### 6. Propose Updates
Based on analysis, propose specific changes to each file.
Focus heavily on:
- **activeContext.md** - Current work, recent changes, next steps
- **progress.md** - Move completed items, update status

### 7. Wait for Confirmation
Present proposal, wait for user approval.

### 8. Apply Updates
Update files based on approved changes.

### 9. Validate Result
```bash
python scripts/validate_memorybank.py /path/to/project
```

## When to Use

- After implementing significant changes
- When new patterns/decisions made
- User explicitly requests update
- After multiple tasks completed

See `scripts/README.md` for complete documentation.
