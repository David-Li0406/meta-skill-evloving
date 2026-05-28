# GitFlow Recommendations

GitFlow branching strategy aligned with sprint planning and Jira workflow integration.

## Branch Strategy Overview

```
main ────────────────────────────────────────→ Production
  │
  └─ release/v1.2.0 ─────────────────────────→ Release prep
       │
develop ─────────────────────────────────────→ Integration
  │
  ├─ feature/PROJ-123-user-auth ─────────────→ Sprint work
  ├─ feature/PROJ-124-payment-flow ──────────→ Sprint work
  └─ fix/PROJ-125-null-check ────────────────→ Bug fixes
```

## Sprint-Aligned Branching

### Feature Branches

```
Naming: feature/<issue-key>-<short-description>

Examples:
feature/PROJ-123-add-login
feature/PROJ-124-user-dashboard
feature/PROJ-125-payment-integration
```

### Branch Lifecycle

| Sprint Phase | Branch Action | Jira Status |
|--------------|---------------|-------------|
| Planning | Create from develop | To Do |
| Development | Active work | In Progress |
| Review | PR created | In Review |
| Done | Merged to develop | Done |

## Sprint Planning Integration

### Pre-Sprint

```
1. Ensure develop is stable
2. All previous sprint branches merged
3. No stale branches older than 1 sprint
4. Release branches created if shipping
```

### During Sprint

```
Day 1-2:
- Create branches for sprint items
- Link branches to Jira issues

Day 3-8:
- Regular commits with issue references
- PR reviews as work completes

Day 9-10:
- Final merges to develop
- Clean up completed branches
```

### Post-Sprint

```
1. All Done items merged
2. Spillover branches documented
3. develop branch tested
4. Release branch if applicable
```

## Branch Health Indicators

### Stale Branch Detection

| Age | Status | Action |
|-----|--------|--------|
| <5 days | Normal | Continue work |
| 5-10 days | Warning | Check for blockers |
| 10-14 days | Alert | Escalate or close |
| >14 days | Critical | Mandatory review |

### Branch Hygiene Rules

```
DO:
- One issue per branch
- Descriptive names with issue key
- Regular rebases from develop
- Delete after merge

DON'T:
- Mix multiple features
- Use generic names (fix, update)
- Let branches go stale
- Force push to shared branches
```

## Release Planning

### Release Branch Workflow

```
When: Sprint end or release milestone
From: develop
Naming: release/v<major>.<minor>.<patch>

Steps:
1. Create release/vX.Y.Z from develop
2. Only bug fixes allowed
3. Merge to main when ready
4. Tag main with version
5. Back-merge to develop
```

### Hotfix Workflow

```
When: Critical production issue
From: main
Naming: hotfix/<issue-key>-<description>

Steps:
1. Create hotfix branch from main
2. Fix and test
3. Merge to main AND develop
4. Tag main with patch version
```

## Jira Issue Linking

### Commit Messages

```
Format: <type>(<scope>): <description>

References: #<issue-key> or PROJ-123

Examples:
feat(auth): add login endpoint

Implements PROJ-123

fix(api): handle null response

Fixes PROJ-456
```

### Automated Linking

| Jira Pattern | Effect |
|--------------|--------|
| PROJ-123 in commit | Links commit to issue |
| PROJ-123 in branch name | Links branch to issue |
| PROJ-123 in PR title | Links PR to issue |
| Fixes PROJ-123 | May auto-transition issue |

## Sprint Velocity Impact

### Branch Metrics

Track for planning:

```
- Average branch lifespan
- PRs merged per sprint
- Code review turnaround
- Merge conflict frequency
```

### Healthy Team Patterns

| Metric | Target | Action if Off |
|--------|--------|---------------|
| Branch lifespan | <5 days | Break down stories |
| PR review time | <1 day | Add reviewers |
| Conflicts/sprint | <2 | Improve coordination |
| Stale branches | 0 | Sprint cleanup task |

## Multi-Project Dependencies

### Cross-Project Branches

```
When PROJ-A depends on INFRA-B:

1. INFRA-B feature completed first
2. INFRA-B merged to develop
3. PROJ-A rebases to get changes
4. PROJ-A completes with dependency

Timeline alignment is critical!
```

### Dependency Branch Strategy

| Scenario | Strategy |
|----------|----------|
| Same sprint | Sequence work appropriately |
| Blocker | Prioritize dependency |
| External team | Coordinate release timing |
| API change | Version and feature flag |

## Best Practices Summary

```
1. One branch per issue
2. Include issue key in branch name
3. Regular syncs with develop
4. Clean up after merge
5. Never commit directly to main
6. PRs require review before merge
7. Keep branches short-lived
8. Document any deviations
```
