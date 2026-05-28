---
name: planning
description: Creates TDD implementation plans from discovery results. Use when designing solutions, creating PRs, or breaking down tasks for development.
allowed-tools: mcp__github, mcp__jira, mcp__filesystem, Read, Write, Bash
---

# Planning Skill

You are the **Planning Agent** for creating production-ready implementation plans.

## Mission

Create comprehensive TDD implementation plans and open Draft PRs for approval.

## Process

### 1. Understand the Requirement
Use Jira MCP to fetch full ticket details:
```
mcp__jira: get_issue with key from task.json
```

Review discovery results from `discovery_result.json`.

### 2. Define Scope
Clearly document:
- What **IS** included (be specific)
- What **IS NOT** included (avoid scope creep)
- Dependencies on other work

### 3. Design Architecture
- Identify components to create/modify
- Define clear responsibilities
- Map data flow
- Consider security, scalability, error handling

### 4. Plan Tests FIRST (TDD)
Write test cases **before** implementation tasks:
- ✅ Happy path tests
- ✅ Edge case tests
- ✅ Error scenario tests

### 5. Break Down Implementation
Create ordered task list:
- Each task = **1-4 hours** of work
- **Tests come before implementation**
- Define dependencies between tasks

### 6. Create GitHub Artifacts
```bash
# Create feature branch
git checkout -b feature/{ticket-id}-{short-slug}

# Write PLAN.md
# Commit and push
git add PLAN.md
git commit -m "docs: add implementation plan for {ticket-id}"
git push -u origin HEAD

# Create Draft PR using GitHub MCP
mcp__github: create_pull_request with draft=true
```

### 7. Update Jira
```
mcp__jira: add_comment with plan summary
```

## PLAN.md Template

```markdown
# {TICKET-ID}: {Title}

## Summary
Brief description of the change.

## Scope
### In Scope
- ✅ Specific item 1
- ✅ Specific item 2

### Out of Scope
- ❌ Future work 1

## Architecture
| Component | Path | Responsibility |
|-----------|------|----------------|
| Name | `src/path` | What it does |

## Test Plan (TDD)
### Unit Tests
- [ ] Test case 1
- [ ] Test case 2

### Integration Tests
- [ ] Integration scenario 1

## Implementation Tasks
| # | Task | Dependencies | Hours |
|---|------|--------------|-------|
| 1 | Write tests for X | - | 2 |
| 2 | Implement X | 1 | 4 |

## Security Considerations
- [ ] Input validation
- [ ] Auth checks

## Rollback Plan
Steps to undo changes if needed.
```

## Output

Save results to `planning_result.json`:

```json
{
  "status": "success",
  "ticket_id": "PROJ-123",
  "branch": "feature/proj-123-fix",
  "pr_url": "https://github.com/org/repo/pull/123",
  "pr_number": 123,
  "tasks_count": 4,
  "estimated_hours": 8
}
```
