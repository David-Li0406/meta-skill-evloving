# ACT Sprint Workflow Skill

Streamline your daily development workflow with sprint planning, standups, health monitoring, and issue automation.

## Quick Start

```bash
# Daily standup report
/sprint-workflow today

# Plan next sprint
/sprint-workflow plan

# Check system health
/sprint-workflow health

# Create issue with auto-detection
/sprint-workflow create Add email notifications
```

## Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `plan` | Sprint planning with velocity analysis | `/sprint-workflow plan` |
| `today` or `standup` | Daily standup report | `/sprint-workflow today` |
| `health` | System health check (all 6 projects) | `/sprint-workflow health` |
| `create <title>` | Create issue with auto-fields | `/sprint-workflow create Fix login bug` |

## Features

### Sprint Planning
- Calculates team velocity from last 3 sprints
- Recommends backlog issues that fit capacity
- Shows breakdown by Type, Project, Repository
- One-click sprint assignment

### Daily Standup
- Yesterday's completed work (from git commits)
- Today's assigned issues
- Sprint progress percentage
- Recent deployments
- Blockers identification

### Health Monitoring
- 6 projects × 4 indicators matrix
- Deployment age tracking
- HTTP status checks
- Database connectivity
- Registry sync status
- Actionable warnings

### Issue Automation
- Auto-detects Type from title keywords
- Auto-assigns Priority based on urgency words
- Auto-estimates Effort (S/M/L/XL)
- Auto-assigns ACT Project from context
- One-step creation + GitHub Projects + Notion sync

## Data Sources

- **GitHub Projects API** - Issues, sprints, fields
- **Dashboard APIs** - Velocity, burndown, health metrics
- **Supabase** - Sprint snapshots, historical data
- **Git** - Local commits, current repo context

## Setup

All required environment variables are already configured:
- ✅ `GITHUB_TOKEN`
- ✅ `GITHUB_PROJECT_ID`
- ✅ `NEXT_PUBLIC_SUPABASE_URL`
- ✅ `SUPABASE_SERVICE_ROLE_KEY`

## Examples

**Morning routine**:
```
/sprint-workflow today
```
Shows what you did yesterday and what's on your plate today.

**Planning session**:
```
/sprint-workflow plan
```
Get data-driven recommendations for next sprint based on velocity.

**Before standup meeting**:
```
/sprint-workflow health
```
Quick check that all systems are running smoothly.

**Creating issues**:
```
/sprint-workflow create Add webhook signature verification
```
Auto-detects: Type=Enhancement, Priority=High (security keyword), Effort=M

## Related

- Full documentation: [SKILL.md](./SKILL.md)
- Quick reference: [QUICK-REFERENCE.md](./QUICK-REFERENCE.md)
- Dashboard: http://localhost:3001/admin/dashboard
