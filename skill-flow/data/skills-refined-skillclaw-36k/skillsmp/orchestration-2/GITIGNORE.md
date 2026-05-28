# Clorch .gitignore Template

Add these patterns to your project's `.gitignore` if using Clorch orchestration.

## Recommended .gitignore Additions

```gitignore
# ===========================================
# Clorch - Claude Orchestration Generated Files
# ===========================================

# Session transcripts (large JSON logs)
.claude/projects/

# Agent output cache
.claude/cache/

# Temporary research/scratch
thoughts/temp/
thoughts/scratch/
thoughts/*/research/

# Handoff files (session-specific, can be large)
thoughts/shared/handoffs/

# Keep these tracked (valuable):
# - thoughts/shared/plans/     (implementation plans)
# - thoughts/ledgers/          (continuity ledgers)
```

## Quick Setup

Run this in your project root:

```bash
cat >> .gitignore << 'EOF'

# Clorch generated files
.claude/projects/
.claude/cache/
thoughts/temp/
thoughts/scratch/
thoughts/*/research/
thoughts/shared/handoffs/
EOF
```

## What Each Directory Contains

| Directory | Content | Track? |
|-----------|---------|--------|
| `.claude/projects/` | Session JSONL transcripts | No (large) |
| `.claude/cache/` | Agent outputs, batch queue | No |
| `thoughts/temp/` | Temporary exploration | No |
| `thoughts/scratch/` | Scratch notes | No |
| `thoughts/*/research/` | Research artifacts | No |
| `thoughts/shared/handoffs/` | Session handoff YAMLs | No* |
| `thoughts/shared/plans/` | Implementation plans | **Yes** |
| `thoughts/ledgers/` | Continuity ledgers | **Yes** |

*Handoffs are session-specific and can be regenerated. Track if you want history.

## Why Track Some Files?

**thoughts/shared/plans/** - Implementation plans:
- Architectural decisions documented
- Step-by-step implementation guides
- Useful for code review and onboarding

**thoughts/ledgers/** - Continuity ledgers:
- Project state preservation
- Cross-session context
- What was working, what was broken

## Full Clorch + Ralph Gitignore

For projects using both:

```gitignore
# ===========================================
# Clorch + Ralph Generated Files
# ===========================================

# Ralph (logs, cache)
.ralph/activity.log
.ralph/cost.log
.ralph/analysis-meta.json
.ralph/project-context.md
.ralph/history/

# Clorch (transcripts, cache)
.claude/projects/
.claude/cache/
thoughts/temp/
thoughts/scratch/
thoughts/*/research/
thoughts/shared/handoffs/

# Track these:
# - .ralph/task.md, prompt.md, guardrails.md
# - thoughts/shared/plans/
# - thoughts/ledgers/
```
