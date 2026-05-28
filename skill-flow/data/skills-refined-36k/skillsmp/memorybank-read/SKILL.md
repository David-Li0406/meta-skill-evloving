---
name: memorybank-read
description: Quick overview of Memory Bank state. Validates structure, reads all 6 files in hierarchical order, and presents formatted summary with staleness warnings.
---

# Memory Bank: Read

Quick overview of current Memory Bank state.

**Helper Scripts Available:**
- `scripts/validate_memorybank.py` - Structure validation
- `scripts/detect_stale.py` - Staleness check

## Workflow

### 1. Validate
```bash
python scripts/validate_memorybank.py /path/to/project
```

### 2. Check Staleness
```bash
python scripts/detect_stale.py /path/to/project
```

### 3. Read Files in Order
Read following the hierarchy:
1. projectbrief.md → Foundation
2. productContext.md → Product vision
3. techContext.md → Technical setup
4. systemPatterns.md → Architecture
5. activeContext.md → Current work
6. progress.md → Status

### 4. Present Summary

```
Memory Bank Summary
===================

Status: ✓ Valid (or ⚠ Issues detected)

## Project Brief
- Purpose: [Brief description]
- Key Objectives: [List]

## Product Context
- User Problems: [Summary]
- Key Features: [List]

## Technical Context
- Stack: [Technologies]
- Key Dependencies: [List]

## System Patterns
- Architecture: [Overview]
- Key Decisions: [List]

## Active Context (Updated: YYYY-MM-DD)
- Current Focus: [What's being worked on]
- Blockers: [Issues]
- Next Steps: [Actions]

## Progress
- What's Working: [Successes]
- What's Left: [Remaining work]
- Status: [Overall state]

## Health Check
- Validation: ✓ Passed
- Staleness: [Score]
- Warnings: [Count]
```

See `scripts/README.md` for complete documentation.
