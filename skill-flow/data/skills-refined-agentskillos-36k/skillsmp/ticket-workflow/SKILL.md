---
name: ticket-workflow
description: ScoreVision's Jira workflow reference—ticket states, allowed transitions, and when to move tickets through the pipeline
---

# ScoreVision Ticket Workflow

This document describes ScoreVision's Jira workflow states, transitions, and conventions.

## Workflow States

| Status | Description |
|--------|-------------|
| To Do | Work not yet started |
| In Progress | Actively being worked on |
| In Development | Code is being written |
| On Hold | Blocked or paused |
| In Review | Code review in progress |
| Ready for QA | Awaiting QA verification |
| Done | Work complete and verified |

## Status Categories

For JQL queries, statuses map to these categories:

- **To Do**: `statusCategory = 'To Do'`
- **In Progress**: `statusCategory = 'In Progress'` (includes In Development, In Review, Ready for QA, On Hold)
- **Done**: `statusCategory = Done`

## Valid Transitions

| Current Status | Scenario | Target Status |
|----------------|----------|---------------|
| To Do | Starting work | In Progress |
| In Progress | Code being written | In Development |
| In Progress | Work complete | In Review |
| In Progress | Work complete, needs QA | Ready for QA |
| In Progress | Blocked | On Hold |
| In Development | Code complete | In Review |
| In Development | Blocked | On Hold |
| On Hold | Unblocked | In Progress |
| In Review | Approved | Done |
| In Review | Approved, needs QA | Ready for QA |
| Ready for QA | QA passed | Done |

## Common JQL Patterns

```sql
-- My open tickets
project = <PROJECT> AND assignee = currentUser() AND resolution = Unresolved

-- Tickets in active development
project = <PROJECT> AND status = 'In Development'

-- All in-progress work
project = <PROJECT> AND statusCategory = 'In Progress'

-- Ready for review
project = <PROJECT> AND status = 'In Review'

-- Current sprint
project = <PROJECT> AND Sprint = '<sprint-name>'
```

## Ticket Review Categorization

When reviewing tickets against codebase state, categorize by:

1. **In Progress** - Actively being worked on
2. **Blocked/On Hold** - Waiting on external dependency or clarification
3. **To Do/Backlog** - Ready to start
4. **In Review** - Code review or QA in progress

## Transition Triggers

| Trigger | Action |
|---------|--------|
| Work complete | Transition to In Review or Ready for QA |
| Blocked by dependency | Transition to On Hold |
| Blocker resolved | Transition back to In Progress |
| Code merged and deployed | Transition to Done |
