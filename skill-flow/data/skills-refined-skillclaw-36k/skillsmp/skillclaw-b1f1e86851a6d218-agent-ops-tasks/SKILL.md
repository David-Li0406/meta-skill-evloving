---
name: agent-ops-tasks
description: Use this skill when you need to create, refine, and manage issues, whether from loose ideas or through bulk operations and JSON export.
---

# Issue Management

**Works with or without `aoc` CLI installed.** All operations can be performed via direct file editing.

## CRITICAL: Issue Management ONLY

**This skill manages issues. It NEVER implements code.**

- ✅ Create, refine, list, search, triage issues
- ✅ Move issues between priority files  
- ❌ **NEVER implement features or fix bugs**
- ❌ **NEVER modify code files**

After any issue operation, ALWAYS offer a handoff — never auto-proceed.

**Reference**: See [REFERENCE.md](REFERENCE.md) for templates, CLI commands, JSON export.

---

## Issue ID Format

**Format**: `{TYPE}-{NUMBER}@{HASH}`  
**Example**: `BUG-0023@efa54f`, `FEAT-0001@c2d4e6`

Types: `BUG` | `FEAT` | `CHORE` | `ENH` | `SEC` | `PERF` | `DOCS` | `TEST` | `REFAC` | `PLAN`

---

## Minimal Issue Template

```yaml
## {TYPE}-{NUMBER}@{HASH} — {title}

id: {TYPE}-{NUMBER}@{HASH}
title: "{title}"
type: {type}
status: todo | in_progress | done
priority: critical | high | medium | low
description: {brief description}
details: references/{TYPE}-{NUMBER}@{HASH}.md

### Acceptance Criteria
- [ ] Criterion 1

### Log
- YYYY-MM-DD: Created
```

---

## Issue Size Guardrails

- Keep backlog items **minimal**: title, metadata, 1–2 sentence description, acceptance criteria if known.
- If an issue needs more than ~20 lines, **move details to a reference file** in `.agent/issues/references/` and link it in the issue.
- Reference files should contain research, long descriptions, examples, diagrams, or interview notes.
- Never embed large code blocks or research dumps directly in backlog items.

### Reference File Format

- Path: `.agent/issues/references/{ISSUE-ID}.md`
- Include a short header and a link back to the issue.
- Example:

```
# {ISSUE-ID} — {title}

Moved from backlog.md on YYYY-MM-DD.

## Context
...
```

---

## File Organization

| File | Priority |
|------|----------|
| `.agent/issues/critical.md` | Blockers, production issues |
| `.agent/issues/high.md` | Important, address soon |
| `.agent/issues/medium.md` | Standard work |
| `.agent/issues/low.md` | Nice-to-have |
| `.agent/issues/backlog.md` | Unprioritized items |