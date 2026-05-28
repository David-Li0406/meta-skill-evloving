# Handoff Note Format

Structured notes for worker-to-conductor communication. Workers write handoff notes before closing issues to provide context for conductors and gates.

## When to Write Handoffs

**Always** add a handoff before closing an issue:

```bash
bd update ISSUE --notes "$(cat <<'NOTES'
## Handoff

**Status**: done
**Summary**: Implemented feature X with tests

### Changes
- file.ts: Added validation logic
NOTES
)"

bd close ISSUE --reason "Done: Implemented feature X"
```

## Handoff Format

```markdown
## Handoff

**Status**: done | blocked | needs_review
**Summary**: Brief description of what was done

### Changes
- file1.ts: Added validation
- file2.ts: Fixed null check
- styles.css: Updated layout

### Discovered Work
- Created follow-up: bd-xyz (edge case handling)
- Created follow-up: bd-abc (related refactor)

### Concerns
- Auth flow might need review before merge
- Performance not tested with large datasets

### Retro
- What was unclear: Initial requirements for edge cases
- Missing context: Didn't know about existing validation util
- What would help: More test cases in the prompt
```

## Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| **Status** | Yes | `done`, `blocked`, or `needs_review` |
| **Summary** | Yes | One-line description of work completed |
| **Changes** | Yes | List of files modified with what changed |
| **Discovered Work** | No | Issues created during work |
| **Concerns** | No | Issues for reviewer/conductor attention |
| **Retro** | Recommended | Learnings for future similar work |

## Status Values

| Status | Meaning | Conductor Action |
|--------|---------|------------------|
| `done` | Work complete, tests pass | Proceed to merge review |
| `blocked` | Cannot continue, needs help | Investigate and reassign |
| `needs_review` | Complete but uncertain | Thorough review before merge |

## Examples

### Simple Bug Fix

```markdown
## Handoff

**Status**: done
**Summary**: Fixed null check in user profile loader

### Changes
- src/profile.ts: Added null guard on line 45

### Retro
- Straightforward fix, no issues
```

### Feature Implementation

```markdown
## Handoff

**Status**: done
**Summary**: Added dark mode toggle with persistence

### Changes
- src/settings.tsx: Added toggle component
- src/theme.ts: Theme context with localStorage sync
- src/styles/dark.css: Dark mode variables

### Discovered Work
- Created: bd-xyz (system preference detection)

### Concerns
- Needs visual QA on all pages

### Retro
- What was unclear: Where to store preference (chose localStorage)
- What would help: Link to design mockups
```

### Blocked Work

```markdown
## Handoff

**Status**: blocked
**Summary**: Cannot complete - API endpoint returns 500

### Changes
- src/api.ts: Started integration (incomplete)

### Concerns
- Backend API /api/users returns 500 error
- Blocking issue needs backend team

### Retro
- Missing context: API docs were outdated
```
