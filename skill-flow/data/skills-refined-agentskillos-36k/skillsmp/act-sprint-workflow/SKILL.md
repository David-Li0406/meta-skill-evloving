---
name: act-sprint-workflow
description: Sprint planning, daily standups, health monitoring, and issue automation for ACT ecosystem development.
---

# ACT Sprint Workflow

## When Triggered
- Sprint planning or backlog review
- Daily standup ("what should I work on?")
- System health checks across projects
- Creating new issues with auto-detection
- Velocity, burndown, or capacity questions

## Commands

| Command | Purpose |
|---------|---------|
| `plan` | Recommend issues for next sprint based on velocity |
| `today` / `standup` | Daily report with yesterday's work and today's focus |
| `health` | Check all 6 ACT projects for issues |
| `create <title>` | Create issue with auto-detected fields |

## Quick Reference

### Projects
- Empathy Ledger, JusticeHub, The Harvest
- ACT Farm, Goods, ACT Studio

### Auto-Detection Rules

**Type:**
- "Add", "Create", "Build" → Enhancement
- "Fix", "Resolve", "Broken" → Bug
- "Document", "Research" → Task

**Priority:**
- "Critical", "Security", "Urgent" → Critical
- "Important", "Should" → High
- "Nice to have", "Eventually" → Low
- Default → Medium

**Effort:**
- "Simple", "Quick" → S
- "Complex", "Major", "Refactor" → L
- "Complete overhaul" → XL
- Default → M

## Data Sources
- GitHub Projects GraphQL API
- Dashboard APIs (`/api/dashboard/*`)
- Supabase (sprint_snapshots, velocity views)
- Git log (local commits)

## File References

| Need | Reference |
|------|-----------|
| Velocity calculations | `references/sprint-planning.md` |
| GraphQL queries | `references/github-api-queries.md` |
| Health patterns | `references/health-monitoring.md` |
| Field mappings | `references/issue-automation.md` |
