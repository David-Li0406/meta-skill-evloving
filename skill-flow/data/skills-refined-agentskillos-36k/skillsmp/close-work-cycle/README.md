# generated: 2025-12-25
# System Auto: last updated on: 2025-12-25T15:04:01
# Close Work Cycle Skill

Guides structured work item closure with Definition of Done (DoD) enforcement.

## Overview

This is a **Cycle Skill** that defines the VALIDATE-ARCHIVE-CAPTURE workflow for closing work items per ADR-033.

## Phases

| Phase | Purpose |
|-------|---------|
| VALIDATE | Verify DoD criteria are met |
| ARCHIVE | Update status and move to archive |
| CAPTURE | Store closure summary to memory |

## Usage

**Automatic:** Invoked by `/close` command after work item lookup.

**Manual:**
```
Skill(skill="close-work-cycle")
```

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill definition with phase contracts |
| `README.md` | This documentation |

## Related

- ADR-033: Work Item Lifecycle Governance
- work-creation-cycle: Parallel skill for creation
- implementation-cycle: Parallel skill for implementation
