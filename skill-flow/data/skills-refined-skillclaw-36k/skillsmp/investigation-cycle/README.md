# generated: 2025-12-22
# System Auto: last updated on: 2025-12-22T16:52:19
# Investigation Cycle Skill

Structured workflow for research and discovery tasks in HAIOS.

## Overview

The investigation-cycle skill guides agents through the **HYPOTHESIZE-EXPLORE-CONCLUDE** workflow when conducting research, analyzing problems, or investigating system behavior.

## Usage

```
Skill(skill="investigation-cycle")
```

Or via the implement command with an investigation backlog ID:
```
/implement INV-XXX
```

## The Three Phases

### 1. HYPOTHESIZE
- Verify investigation document exists and is ready
- Define hypotheses to test
- Query memory for prior related work

### 2. EXPLORE
- Execute investigation steps
- Document findings as discovered
- Update hypotheses based on evidence

### 3. CONCLUDE
- Synthesize findings
- Spawn follow-up work items (ADRs, plans, new investigations)
- Store learnings to memory
- Close the investigation

## Related Files

- `SKILL.md` - Full skill definition with exit criteria
- `.claude/templates/investigation.md` - Document template
- `.claude/commands/new-investigation.md` - Creation command

## Parallel Structure

| Investigation | Implementation |
|---------------|----------------|
| HYPOTHESIZE | PLAN |
| EXPLORE | DO |
| CONCLUDE | CHECK + DONE |

## Created

- **Session:** 98
- **Date:** 2025-12-22
- **Backlog:** E2-111
