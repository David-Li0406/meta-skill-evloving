# Linear Best Practices

How to use Linear effectively for issue tracking and project management.

## Core Philosophy

Linear is designed around these principles:

1. **Speed over ceremony** - Minimize friction, maximize flow
2. **Keyboard-first** - Everything is a shortcut away
3. **Opinionated defaults** - Less configuration, more doing
4. **Write it down** - Issues are documentation
5. **Close the loop** - Every issue has an outcome

## Issue Hygiene

### Writing Good Issues

**Title format**: `[Type]: Brief description`

```
Bug: Login button unresponsive on mobile Safari
Feature: Add dark mode toggle to settings
Chore: Upgrade React to v19
Refactor: Extract auth logic into separate module
```

**Description structure**:

```markdown
## Context
Why does this matter? What's the background?

## Requirements
- [ ] Specific, testable requirement
- [ ] Another requirement
- [ ] Acceptance criteria

## Technical Notes
Implementation hints, related code, API docs.

## Out of Scope
What this issue explicitly does NOT cover.
```

### Issue Sizing

Keep issues small and completable in 1-3 days:

| Size | Guideline |
|------|-----------|
| **Too small** | "Fix typo in README" - just do it |
| **Right size** | "Add password reset flow" - clear scope, few days |
| **Too big** | "Implement authentication" - break it down |

If an issue takes more than a week, it's an epic or project, not an issue.

### Breaking Down Work

Use sub-issues for decomposition:

```
Parent: Implement user authentication
├── Sub: Set up auth database schema
├── Sub: Create login API endpoint
├── Sub: Build login form component
├── Sub: Add session management
└── Sub: Write authentication tests
```

Create sub-issues when:
- Parent issue has multiple distinct deliverables
- Work can be parallelized across team members
- You need to track progress on components

## Workflow States

### Standard Flow

```
Backlog → Todo → In Progress → In Review → Done
```

| State | Meaning | Action |
|-------|---------|--------|
| **Backlog** | Ideas, not committed | Triage regularly |
| **Todo** | Committed for this cycle | Ready to start |
| **In Progress** | Actively working | Limit WIP |
| **In Review** | Awaiting review/QA | Quick turnaround |
| **Done** | Shipped/verified | Celebrate |
| **Canceled** | Won't do | Document why |

### State Discipline

**One issue In Progress at a time** per person. Context switching kills productivity.

```bash
# Check your WIP
linctl issue list --assignee me --state "In Progress" --json | jq 'length'
# Should be 1 (maybe 2 max)
```

**Move blocked issues** to a Blocked state or add a label. Don't let them rot In Progress.

**Canceled ≠ failure** - Document why and move on. Better than zombie issues.

## Priority Framework

### When to Use Each Priority

| Priority | Use For | Response Time |
|----------|---------|---------------|
| **Urgent (1)** | Production down, data loss, security | Drop everything |
| **High (2)** | Blocking other work, important deadlines | This week |
| **Normal (3)** | Standard work, planned features | This cycle |
| **Low (4)** | Nice to have, improvements | When time permits |
| **None (0)** | Backlog, ideas | Triage later |

### Priority Anti-patterns

❌ **Everything is urgent** - If everything is P1, nothing is P1
❌ **Priority inflation** - "This is important to me" ≠ urgent
❌ **Stale priorities** - Re-evaluate when context changes

```bash
# Find priority inflation
linctl issue list --priority 1 --json | jq 'length'
# More than 5 urgent issues? Time to triage.
```

## Cycles (Sprints)

### Cycle Planning

1. **Pull from backlog** - Don't create new issues during planning
2. **Capacity check** - Points/count based on historical velocity
3. **Dependencies first** - Identify blockers before committing
4. **Buffer for surprises** - 80% planned, 20% slack

### During the Cycle

- **Daily check**: What's blocked? What's done?
- **Mid-cycle review**: Are we on track? Scope cut?
- **No scope creep**: New ideas go to backlog, not current cycle

### Cycle Retrospective

- What shipped?
- What didn't? Why?
- What should change?

## Labels

### Effective Label Strategy

Keep labels minimal and meaningful:

| Category | Examples | Purpose |
|----------|----------|---------|
| **Type** | `bug`, `feature`, `chore` | What kind of work |
| **Area** | `frontend`, `api`, `infra` | Where in codebase |
| **Status** | `blocked`, `needs-review` | Current state modifier |

### Label Anti-patterns

❌ **Too many labels** - If you have 50 labels, you have 0 useful labels
❌ **Redundant labels** - Don't duplicate state with labels
❌ **Abandoned labels** - Audit and remove unused labels quarterly

## Projects

### When to Create a Project

Create a project when:
- Multiple issues toward a shared goal
- Needs tracking across cycles
- Has a defined end state
- Multiple people/teams involved

Don't create a project for:
- Single issues
- Ongoing maintenance
- "Everything frontend-related"

### Project Structure

```
Initiative: 2024 Growth
├── Project: User Onboarding Revamp
│   ├── Issue: Redesign welcome flow
│   ├── Issue: Add progress indicators
│   └── Issue: Implement email sequences
├── Project: Mobile App Launch
│   ├── Issue: Set up React Native
│   └── ...
```

### Project Health

Track these metrics:

```bash
# Project progress
linctl project get <uuid> --json | jq '{
  name,
  progress: "\(.progress * 100 | floor)%",
  completed: .issueCountHistory.completed,
  remaining: (.scope - .issueCountHistory.completed)
}'
```

Healthy projects:
- Progress matches time elapsed
- Issues moving through states
- No issues stuck > 1 week

## Team Collaboration

### Assignment Practices

| Scenario | Approach |
|----------|----------|
| **New issue** | Assign during triage, not creation |
| **Pair work** | Assign primary owner, mention partner |
| **Handoff** | Reassign + comment with context |
| **Stuck** | Keep assigned, add blocked label |

### Communication in Issues

**Comment for**:
- Status updates ("Started investigating")
- Questions ("@jane what's the expected behavior?")
- Context ("Found the root cause: ...")
- Handoffs ("Passing to @john for review")

**Don't comment for**:
- "Working on this" (just move to In Progress)
- "+1" or "agree" (use reactions)
- Long discussions (move to Slack/doc, link back)

### Mentions and Notifications

Use `@mentions` intentionally:
- `@person` - Need their input/action
- Don't mass-mention - Creates noise

## Triage Process

### Daily Triage (5 min)

```bash
# New unassigned issues
linctl issue list --assignee unassigned --newer-than 1_day_ago --json

# Action: Assign owner, set priority
```

### Weekly Triage (30 min)

```bash
# Stale in-progress issues
linctl issue list --state "In Progress" --newer-than all_time --json | \
  jq '.[] | select(.updatedAt < (now - 7*24*60*60 | todate))'

# Backlog grooming
linctl issue list --state "Backlog" --json | jq 'length'
# > 50 items? Time to close or prioritize.
```

### What to Do

| Issue State | Action |
|-------------|--------|
| New, valid | Assign, prioritize, estimate |
| New, unclear | Ask clarifying questions |
| New, duplicate | Close, link to original |
| New, won't fix | Close with explanation |
| Stale backlog | Close or promote to Todo |
| Stuck in progress | Unblock or reassign |

## Common Workflows

### Bug Reports

```bash
# 1. Create with context
linctl issue create \
  --title "Bug: Users logged out unexpectedly" \
  --team ENG \
  --priority 2 \
  --description "## Reproduction
1. Log in
2. Wait 5 minutes
3. Refresh page

## Expected
Stay logged in

## Actual
Redirected to login

## Impact
~100 reports this week"

# 2. Investigate and update
linctl comment create LIN-123 --body "Root cause: Session TTL set to 5min instead of 5hr"

# 3. Link fix
linctl comment create LIN-123 --body "Fixed in PR #456"

# 4. Close
linctl issue update LIN-123 --state "Done"
```

### Feature Development

```bash
# 1. Refine requirements (in issue description)
# 2. Break into sub-issues if needed
# 3. Start work
linctl issue update LIN-100 --state "In Progress" --assignee me

# 4. Branch from issue
git checkout -b $(linctl issue get LIN-100 --json | jq -r '.branchName')

# 5. Regular updates
linctl comment create LIN-100 --body "Backend complete, starting frontend"

# 6. Ready for review
linctl issue update LIN-100 --state "In Review"
linctl comment create LIN-100 --body "PR ready: https://github.com/..."

# 7. Ship it
linctl issue update LIN-100 --state "Done"
```

### Incident Response

```bash
# 1. Create urgent issue immediately
linctl issue create \
  --title "INCIDENT: Database connection failures" \
  --team ENG \
  --priority 1 \
  --assign-me

# 2. Live updates as comments
linctl comment create LIN-999 --body "Investigating. @oncall joining."
linctl comment create LIN-999 --body "Found: Connection pool exhausted"
linctl comment create LIN-999 --body "Mitigated: Restarted services, increased pool"
linctl comment create LIN-999 --body "Resolved: Services stable. RCA to follow."

# 3. Post-mortem
linctl issue update LIN-999 --description "...(add RCA)..."
linctl issue update LIN-999 --state "Done"
```

## Anti-patterns to Avoid

### Issue Anti-patterns

| Anti-pattern | Problem | Fix |
|--------------|---------|-----|
| **Ghost issues** | Created, never touched | Weekly triage |
| **Mega issues** | Too big to complete | Break down |
| **Vague issues** | "Fix the thing" | Require clear scope |
| **Duplicate issues** | Same problem, multiple tickets | Search first |
| **Issue as chat** | 50 comments, no progress | Move discussion elsewhere |

### Process Anti-patterns

| Anti-pattern | Problem | Fix |
|--------------|---------|-----|
| **Estimate theater** | Hours spent estimating | T-shirt sizes or skip |
| **Ceremony overload** | More meetings than coding | Async updates |
| **Dashboard addiction** | Pretty charts, no action | Focus on doing |
| **Inbox zero obsession** | Processing over producing | Batch notifications |

## Metrics That Matter

### Team Health

```bash
# Cycle time (how long from start to done)
# Throughput (issues completed per cycle)
# WIP (issues in progress right now)

linctl issue list --state "In Progress" --team ENG --json | jq 'length'
```

### Warning Signs

| Metric | Warning | Action |
|--------|---------|--------|
| WIP > team size | Too much in flight | Finish before starting |
| Cycle time increasing | Process friction | Remove blockers |
| Backlog growing | Scope creep | Aggressive triage |
| Done count dropping | Team struggles | Check blockers, morale |

## Quick Reference

### Daily Habits

1. Check assigned issues
2. Update status (state + comments)
3. Triage new mentions
4. Clear notifications

### Weekly Habits

1. Review cycle progress
2. Triage backlog
3. Close stale issues
4. Plan next priorities

### Healthy Limits

| Item | Guideline |
|------|-----------|
| WIP per person | 1-2 issues |
| Backlog size | < 50 issues |
| Issue age in progress | < 1 week |
| Urgent issues | < 5 total |
| Labels per team | < 15 |
