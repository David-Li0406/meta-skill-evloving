# Completion Promises

Ralph loops use completion promises to signal when work is done. The promise format must match exactly for the loop to recognize completion.

## Promise Formats by Mode

| Mode | Promise | When to Output |
|------|---------|----------------|
| **PRD** | `<promise>ALL STORIES PASS</promise>` | All user stories pass their acceptance criteria |
| **Plan** | `<promise>ALL PHASES COMPLETE</promise>` | All phases pass their verification |
| **Freeform** | `<promise>TASK COMPLETE</promise>` | The task goal is achieved |

## Usage Rules

1. **Only output when truly complete** - Never output a promise if work remains
2. **Exact format required** - The tags and text must match exactly
3. **One promise per loop** - Output the promise once at the very end
4. **No partial promises** - Either all criteria pass or no promise is output

## Examples

### PRD Mode (User Stories)
```
All 4 user stories now pass their acceptance criteria:
- US-001: User registration ✓
- US-002: Email verification ✓  
- US-003: Password reset ✓
- US-004: Profile update ✓

<promise>ALL STORIES PASS</promise>
```

### Plan Mode (Phases)
```
All phases are now complete:
- P1: Research existing patterns ✓
- P2: Implement core logic ✓
- P3: Add error handling ✓

<promise>ALL PHASES COMPLETE</promise>
```

### Freeform Mode
```
The task is complete:
- Fixed the authentication bug
- Added test coverage
- Verified in development environment

<promise>TASK COMPLETE</promise>
```

## Anti-Patterns

**Never do these:**

```markdown
<!-- WRONG: Partial completion -->
<promise>STORIES 1-3 PASS</promise>

<!-- WRONG: Different wording -->
<promise>DONE</promise>
<promise>COMPLETE</promise>

<!-- WRONG: Missing tags -->
ALL STORIES PASS

<!-- WRONG: Promise when blocked -->
Story US-003 is blocked, but other stories pass.
<promise>ALL STORIES PASS</promise>
```
