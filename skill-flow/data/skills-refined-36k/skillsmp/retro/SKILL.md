---
name: retro
description: This skill should be used when the user asks to "capture learnings", "run retrospective", "log what we learned", "update error history", or at the end of a session to capture insights. Reviews session and selectively logs insights worth preserving.
---

# Session Retrospective

Review the current session and capture learnings. Be selective—only log insights worth preserving for future sessions.

## Tasks

### 1. Error Patterns
If errors occurred:
- Check `.claude/ERROR_HISTORY.md` for existing entries
- Add new entries only if: error spans >2 files, non-obvious root cause, or likely to recur
- Use format: date, type, severity, files, error, root cause, fix, prevention

### 2. Learnings
Update `.claude/LEARNINGS.md` with:
- Patterns that worked well in this codebase
- Conventions discovered (naming, structure, data flow)
- Gotchas or anti-patterns to avoid
- Skip obvious/generic knowledge

### 3. CLAUDE.md Updates
If session revealed:
- New verification commands needed
- Additional paths worth documenting
- MCP tool usage patterns
- Agent strategy improvements

## Entry Formats

### LEARNINGS.md

```markdown
## YYYY-MM-DD: [Brief Topic]

**Context:** [What was being done]
**Learning:** [Key insight]
**Apply when:** [Trigger conditions]
```

### ERROR_HISTORY.md

```markdown
## YYYY-MM-DD: [Error Type]

**Severity:** Low | Medium | High | Critical
**Files:** [Affected files]
**Error:** [Error message/symptom]
**Root Cause:** [What actually caused it]
**Fix:** [How resolved]
**Prevention:** [How to avoid]
```

## Logging Guidelines

**Log if:**
- Error occurred 2+ times
- Error spans multiple files
- Root cause was non-obvious
- Pattern saved significant time
- Would help future debugging

**Skip if:**
- Simple typo or one-off
- Generic/common knowledge
- Already documented
- Temporary workaround

## Quick Checklist

- [ ] Check ERROR_HISTORY.md before logging (avoid duplicates)
- [ ] Check LEARNINGS.md before logging (avoid duplicates)
- [ ] Use terse, imperative language
- [ ] Include when to apply the learning
- [ ] Consider if pattern warrants skill update

---

## Additional Resources

### Reference Files

For detailed guidance:
- **`references/logging-triggers.md`** — What to log, when, and format details
- **`references/skill-evolution.md`** — When to update skills vs log learnings
- **`references/meta-learning.md`** — Reflection questions, retrospective templates

### Scripts

Utility scripts in `scripts/`:
- **`validate-learnings.sh`** — Check for duplicates and stale entries

---

## Quick Reference

### What to Log

| Category | Example | Destination |
|----------|---------|-------------|
| Hook/API quirk | `estimatedTotal` not `total` | LEARNINGS.md |
| Path convention | `layouts/` vs `layout/` | LEARNINGS.md |
| Type pattern | `as const` for variants | LEARNINGS.md |
| Route conflict | Dynamic segment collision | ERROR_HISTORY.md |
| Auth bypass | RLS exception needed | ERROR_HISTORY.md |
| Import issue | Path resolution mismatch | ERROR_HISTORY.md |

### Skill Update Triggers

| If pattern... | Then update... |
|---------------|----------------|
| Motion/animation | frontend-design |
| Question revealed scope | prd-clarify |
| State/affordance | prd-ux |
| Prompt structure | ux-prompts |
| Verification command | CLAUDE.md |

### Common Patterns to Watch

**TypeScript/React:**
- File casing (case-sensitive imports)
- Framework namespace changes
- Instrumentation patterns

**Testing:**
- Browser API mocks (ResizeObserver, matchMedia)
- Exact matching requirements
- Avoid class-based assertions

**Build/Config:**
- Version mismatches
- Path alias resolution
- Environment-specific behavior
