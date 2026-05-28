# Ralph/Clorch .gitignore Template

Add these patterns to your project's `.gitignore`:

## Recommended .gitignore Additions

```gitignore
# ===========================================
# Ralph - Autonomous Loop Generated Files
# ===========================================

# Logs (large, runtime-generated)
.ralph/activity.log
.ralph/cost.log

# Cache files (regenerated on each run)
.ralph/analysis-meta.json
.ralph/project-context.md

# Archived runs (can be large)
.ralph/history/

# Keep these tracked (valuable):
# - .ralph/task.md       (what was requested)
# - .ralph/prompt.md     (instructions used)
# - .ralph/guardrails.md (accumulated learnings)

# ===========================================
# Clorch - Claude Orchestration Files
# ===========================================

# Session transcripts (large JSON logs)
.claude/projects/

# Agent output cache
.claude/cache/

# Temporary research/thinking
thoughts/temp/
thoughts/scratch/
thoughts/*/research/

# Session handoffs (can be large)
thoughts/shared/handoffs/

# Keep these tracked (valuable):
# - thoughts/shared/plans/  (implementation plans)
# - thoughts/ledgers/       (continuity ledgers)
```

See also: `~/.claude/skills/orchestration/GITIGNORE.md` for full Clorch patterns.

## Quick Setup

Run this in your project root:

```bash
cat >> .gitignore << 'EOF'

# Ralph/Clorch generated files
.ralph/activity.log
.ralph/cost.log
.ralph/analysis-meta.json
.ralph/project-context.md
.ralph/history/
.claude/projects/
.claude/cache/
thoughts/temp/
thoughts/scratch/
EOF
```

## What Each File Contains

| File | Content | Track? |
|------|---------|--------|
| `activity.log` | Full Claude output per iteration | No (large) |
| `cost.log` | Cost estimates per iteration | No |
| `analysis-meta.json` | Cache timestamps, hashes | No |
| `project-context.md` | Cached codebase analysis | No |
| `history/` | Archived past runs | No |
| `task.md` | Task definitions | **Yes** |
| `prompt.md` | Static prompt template | **Yes** |
| `guardrails.md` | Learned patterns/warnings | **Yes** |

## Why Track Some Files?

**task.md** - Documents what was requested. Useful for:
- Code review (what did Ralph try to do?)
- Reproducibility (re-run same tasks)
- History (what features were added via Ralph)

**prompt.md** - Documents the context given to Ralph:
- Project-specific instructions
- Stack information
- Command templates

**guardrails.md** - Accumulated project knowledge:
- Patterns that worked
- Mistakes to avoid
- Project-specific rules
