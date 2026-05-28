# Common Workflows

Practical workflow patterns for common Jira use cases and team collaboration.

## Important Note About Transitions and Comments

**WARNING:** Many examples in Jira documentation show using `--comment` flag during transitions (e.g., `jira issue move PROJ-123 Done --comment "Fixed"`). However, this frequently fails with "Field 'comment' cannot be set" errors because most Jira workflows don't expose the comment field on transition screens.

**RECOMMENDED PATTERN:** Always perform transitions and comments as separate operations:

```bash
# Recommended (works reliably)
jira issue move PROJ-123 Done
jira issue comment add PROJ-123 "Fixed in PR #456"

# Not recommended (often fails)
# jira issue move PROJ-123 Done --comment "Fixed in PR #456"
```

All workflow examples below follow the recommended two-step pattern for maximum reliability.

---

## Daily Standup

Quick answers for daily standup:

```bash
# What did I work on yesterday?
jira issue list -a$(jira me) --updated -1d --plain

# What am I working on today?
jira issue list -a$(jira me) -s"In Progress" --plain

# Tickets I closed this week
jira issue list -a$(jira me) -sDone --updated week --plain

# Any blockers? (high priority not done)
jira issue list -a$(jira me) -yHigh -s~Done --plain
```

## Start Working on Issue

Complete workflow to pick up work:

```bash
# 1. Assign to self
jira issue assign PROJ-123 $(jira me)

# 2. Move to In Progress
jira issue move PROJ-123 "In Progress"

# 3. Add comment
jira issue comment add PROJ-123 "Starting work"
```

## Complete Issue

Workflow to close an issue:

```bash
# 1. Log time spent
jira issue worklog add PROJ-123 "4h" --comment "Implementation" --no-input

# 2. Add PR link
jira issue link remote PROJ-123 "https://github.com/org/repo/pull/456" "PR #456"

# 3. Move to review
jira issue move PROJ-123 "In Review"
jira issue comment add PROJ-123 "PR ready for review"

# 4. After approval, close
jira issue move PROJ-123 Done -RFixed
jira issue comment add PROJ-123 "Merged in PR #456"
```

## Code Review Workflow

Integrate Jira with code reviews:

```bash
# 1. Link PR to ticket
jira issue link remote PROJ-123 "https://github.com/org/repo/pull/456" "PR #456"

# 2. Move to review
jira issue move PROJ-123 "In Review"
jira issue comment add PROJ-123 "Ready for code review"

# 3. Add review comments
jira issue comment add PROJ-123 "LGTM! Minor suggestions in PR comments."

# 4. Close after merge
jira issue move PROJ-123 Done -RFixed
jira issue comment add PROJ-123 "Merged"
```

## Bug Triage

Efficient bug handling:

```bash
# List new bugs from last week
jira issue list -tBug -sOpen --created -7d --plain

# List critical/high priority bugs
jira issue list -tBug -yHighest,High -s~Done --plain

# Assign to team lead
jira issue assign BUG-123 "Team Lead"

# Add triage notes
jira issue comment add BUG-123 "Investigating root cause. Checking logs."

# Update priority and labels
jira issue edit BUG-123 -yHigh -lproduction -lurgent --no-input

# Link to related issues
jira issue link BUG-123 BUG-100 "is caused by"
```

## Close as Duplicate

```bash
# 1. Link to original
jira issue link PROJ-123 PROJ-100 Duplicates

# 2. Close with resolution (if available)
jira issue move PROJ-123 Done -RDuplicate
jira issue comment add PROJ-123 "Duplicate of PROJ-100"

# Alternative: Close without resolution
jira issue move PROJ-123 Done
jira issue comment add PROJ-123 "Duplicate of PROJ-100"
```

## Close as Won't Fix

```bash
# With resolution (if available in workflow)
jira issue move PROJ-123 Done -R"Won't Fix"
jira issue comment add PROJ-123 "Out of scope for this release"

# Without resolution
jira issue move PROJ-123 Done
jira issue comment add PROJ-123 "Won't Fix: Out of scope for this release"
```

## Workflow Configuration Differences

Different Jira instances and projects may have different field availability:

- **Resolution field**: Not all workflows include this field. If you encounter "Field 'resolution' cannot be set", simply omit the `-R` flag
- **Comment field during transitions**: Most workflows don't expose comment field on transition screens. Always add comments separately using `jira issue comment add` after transitions
- **Custom fields**: Projects may have custom required fields during transitions
- **Transition names**: State names and transition names can differ (e.g., "In Progress" state might require "Start working" transition)

**Best practice:** Always check available transitions interactively first:

```bash
jira issue move PROJ-123  # Shows available transitions and required fields
```

## Incident Response

Handle production incidents:

```bash
# 1. Create incident ticket
jira issue create -tBug -s"Production outage: API down" -yHighest -lincident -lproduction --no-input

# 2. Link related issues
jira issue link INC-1 BUG-789 "is caused by"

# 3. Add status updates
jira issue comment add INC-1 "Root cause identified. Rolling back deployment."

# 4. Track time spent
jira issue worklog add INC-1 "2h" --comment "Incident response" --no-input

# 5. Close incident
jira issue move INC-1 Done -RFixed
jira issue comment add INC-1 "Service restored. Post-mortem scheduled."
```

## Sprint Planning

Prepare for sprint planning:

```bash
# High priority unassigned (need assignment)
jira issue list -ax -yHigh --plain

# Backlog items ready for sprint
jira issue list -s"Ready for Dev" --order-by rank --reverse --plain

# Current sprint progress
jira sprint list --current --plain

# Add issues to sprint
jira sprint add SPRINT_ID PROJ-123 PROJ-124 PROJ-125
```

## Epic Management

Working with epics:

```bash
# Create epic
jira epic create -n"Q1 Authentication Improvements" -s"Improve auth security" -yHigh --no-input

# Add stories to epic
jira issue create -tStory -s"Implement OAuth2" -PEPIC-42 --no-input
jira epic add EPIC-42 PROJ-100 PROJ-101

# Check epic progress
jira epic list EPIC-42 -sDone --plain --no-headers | wc -l   # Done
jira epic list EPIC-42 --plain --no-headers | wc -l          # Total
```

## Handoff to Another Team Member

```bash
# Reassign
jira issue assign PROJ-123 "jane.doe"

# Add handoff context
jira issue comment add PROJ-123 "Handing off to @jane.doe

**Context:**
- Root cause identified in auth module
- Fix approach discussed in standup
- Related to PROJ-100

**Files to check:**
- src/auth/login.py
- tests/auth/test_login.py"
```

## Block/Unblock Issue

```bash
# Block an issue
jira issue move PROJ-123 Blocked
jira issue comment add PROJ-123 "Waiting on external API access"

# Link blocker
jira issue link PROJ-123 PROJ-456 "is blocked by"

# Unblock
jira issue move PROJ-123 "To Do"
jira issue comment add PROJ-123 "Blocker resolved"
```

## Bulk Operations

Handle multiple issues:

```bash
# Assign multiple issues
for issue in PROJ-123 PROJ-124 PROJ-125; do
  jira issue assign "$issue" $(jira me)
done

# Add label to multiple issues
for issue in PROJ-123 PROJ-124 PROJ-125; do
  jira issue edit "$issue" --label sprint-42 --no-input
done

# Close multiple issues with comments
for issue in PROJ-123 PROJ-124 PROJ-125; do
  jira issue move "$issue" Done -RFixed
  jira issue comment add "$issue" "Sprint cleanup"
done
```

## Personal Productivity Aliases

Add to your shell config:

```bash
# My daily dashboard
alias jira-today='jira issue list -a$(jira me) -s"In Progress" --plain'

# What I should focus on
alias jira-priorities='jira issue list -a$(jira me) -yHigh -s~Done --order-by priority --plain'

# What I reported that needs attention
alias jira-reported='jira issue list -r$(jira me) -s"To Do" --plain'

# My work this week
alias jira-week='jira issue list -a$(jira me) --updated week --plain'

# Quick task creation
alias jira-task='jira issue create -tTask -a$(jira me)'
```
