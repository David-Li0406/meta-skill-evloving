---
name: triage-backlog
description: Use this skill when you need to analyze and prioritize your Linear backlog, identifying stale, blocked, and high-priority issues for effective management.
---

# Triage Skill - Backlog Analysis

You are an expert at analyzing and prioritizing software backlogs.

## When to Use

Use this skill when:
- The backlog needs cleanup
- Prioritization decisions need to be made
- Looking for stale or blocked issues

## Process

### CRITICAL: Setup First
**Ensure team context is set:**
```bash
linear init  # If .linear.yaml doesn't exist
```

1. **Fetch the Backlog**
   ```bash
   linear issues list --state Backlog --format full --limit 100
   ```

2. **Analyze Dependencies**
   ```bash
   linear deps --team ENG
   ```

3. **Filter by Priority**
   ```bash
   # High priority backlog items
   linear issues list --state Backlog --priority 1 --format full

   # Urgent only (P1)
   linear issues list --state Backlog --priority 1 --format full

   # Customer issues
   linear issues list --labels customer --format full

   # Bugs in backlog
   linear issues list --state Backlog --labels bug --format full
   ```

4. **Identify Issues**
   Look for:
   - **Stale issues**: No updates in 30+ days
   - **Blocked issues**: Dependencies not resolved
   - **Priority mismatches**: High priority but blocked
   - **Orphaned issues**: No assignee, no activity

5. **Generate Recommendations**

## Analysis Framework

### Staleness Check
- Last updated > 30 days ago = Stale
- Last updated > 60 days ago = Very stale (consider closing)
- No activity + no assignee = Orphaned

### Dependency Health
- Blocked by completed issues = Unblock
- Circular dependencies = Flag for resolution
- Long blocking chains = Risk

### Priority Assessment
- P1/P2 but blocked = Escalate blocker
- P3/P4 with no activity = Consider closing
- No priority set = Needs triage

## Output Format

```
BACKLOG TRIAGE: Team ENG
════════════════════════════════════════

URGENT ATTENTION (3)
────────────────────────────────────────
ENG-101 [Stale 45d] Login bug - P1 but no activity
ENG-102 [Blocked] Payment flow - blocked by ENG-99
ENG-103 [Orphaned] API refactor - no owner

RECOMMENDED ACTIONS
────────────────────────────────────────
1. Unblock ENG-102: Complete ENG-99 or remove dependency
2. Assign ENG-103: Needs owner or close if abandoned
3. Update ENG-101: Stale P1 needs attention

HEALTH SUMMARY
────────────────────────────────────────
Total issues: 45
Blocked: 8 (17%)
Stale: 12 (26%)
Healthy: 25 (55%)
```

## Commands Used

```bash
# List all issues for a team
linear issues list --team ENG

# Check dependencies
linear deps --team ENG

# Update priority
linear issues update ENG-123 --priority 2

# Add a comment about triage
linear issues comment ENG-123 --body "Triaged: Needs unblocking before sprint"
```

## Discovery Commands

Use search to discover triage-worthy issues:

```bash
# Find all blocked issues that need attention
linear search --has-blockers --state "In Progress" --team ENG

# Find high priority work that's blocked
```