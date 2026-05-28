---
name: session-resume-work
description: Use this skill to restore and resume work from a previous session with full context.
---

# Session Resume and Work Restoration Skill

This skill helps agents quickly restore project context and resume work seamlessly from a previous session.

## When To Use

- At the **start of any new conversation**
- When context seems missing
- When the user asks "what were we working on?"
- When the user starts with "continue", "resume", or "where were we"

## Instrumentation

```bash
# Log usage when using this skill
./scripts/log-skill.sh "session-resume-work" "manual" "$$"
```

## Quick Resume Checklist

### 1. Check Active Work

```bash
# Ready todos (highest priority)
ls todos/*-ready-*.md 2>/dev/null | head -5

# In-progress plans
ls plans/*.md 2>/dev/null

# Recent solutions (for context)
ls -t docs/solutions/**/*.md 2>/dev/null | head -3
```

### 2. Check Recent Git Activity

```bash
# Recent commits
git log --oneline -5

# Uncommitted changes
git status --short
```

### 3. Restore Project Context

Follow the resume-project workflow which handles:

1. Project existence verification
2. Loading or reconstructing `STATE.md`
3. Checkpoint detection (.continue-here files)
4. Incomplete work detection (PLAN without SUMMARY)
5. Visual status presentation
6. Context-aware next action routing (checks `CONTEXT.md` before suggesting plan vs discuss)
7. Session continuity updates

### 4. Check System Health

```bash
./scripts/compound-dashboard.sh
```

Review health grade and recommendations before starting work.

### 5. Final Summary

```
📍 Session Context:

**Active Work:**
- {X} ready todos waiting
- Plan in progress: {plan name if any}

**Recent Activity:**
- Last commit: {subject}
- {Changed files if uncommitted}

**Suggested Next Steps:**
1. {Most logical next action}
2. {Alternative}
```

## Automatic Triggers

Consider running this skill when you see:
- User starts with "continue", "resume", "where were we"
- First message in a new session
- User seems to lack context

## References

- Todos: `todos/`
- Plans: `plans/`
- Solutions: `docs/solutions/`
- Workflows: `.agent/workflows/`