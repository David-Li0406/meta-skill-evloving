# Pull Request Templates

Templates for creating Pull Requests with Jira integration using `devflow_git_pr_context`.

## Standard Feature PR

```markdown
## Summary

This PR addresses [PROJ-123](jira-link).

[Description from Jira issue]

## Related Issues

- PROJ-123: [Issue summary]

## Acceptance Criteria

- [ ] [Criteria from Jira issue]
- [ ] [Additional criteria]

## Changes

<!-- Describe the main changes in this PR -->
-

## Testing

- [ ] Unit tests pass locally
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] No regressions in existing functionality
- [ ] Code review completed

**Story Points:** X
```

## Bug Fix PR

```markdown
## Summary

This PR fixes [PROJ-456](jira-link).

### Problem
[Description of the bug from Jira]

### Solution
[Brief explanation of the fix]

## Related Issues

- PROJ-456: [Bug summary]

## Changes

-

## Testing

- [ ] Bug reproduction verified before fix
- [ ] Fix resolves the reported issue
- [ ] No new regressions introduced
- [ ] Edge cases considered and tested
- [ ] Unit tests pass locally
- [ ] Integration tests pass
```

## Hotfix PR

```markdown
## Summary

**HOTFIX** This PR addresses critical issue [PROJ-789](jira-link).

### Severity
[Critical/High] - [Brief impact description]

### Problem
[Description of the issue]

### Solution
[Minimal fix description]

## Related Issues

- PROJ-789: [Issue summary]

## Changes

-

## Testing

- [ ] Critical issue resolved
- [ ] Minimal changes to reduce risk
- [ ] Rollback plan documented
- [ ] Monitoring in place
- [ ] Unit tests pass locally

## Deployment Notes

- Requires immediate deployment
- Rollback procedure: [describe]
```

## Multi-Issue PR

```markdown
## Summary

This PR addresses the following issues:

- [PROJ-123](jira-link): [Summary 1]
- [PROJ-124](jira-link): [Summary 2]
- [PROJ-125](jira-link): [Summary 3]

## Related Issues

- PROJ-123: [Summary]
- PROJ-124: [Summary]
- PROJ-125: [Summary]

## Acceptance Criteria

### PROJ-123
- [ ] [Criteria]

### PROJ-124
- [ ] [Criteria]

### PROJ-125
- [ ] [Criteria]

## Changes

-

## Testing

- [ ] All acceptance criteria met
- [ ] Unit tests pass locally
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Code review completed

**Total Story Points:** X
```

## Using devflow_git_pr_context

Generate PR context automatically:

```
devflow_git_pr_context(
  issueKeys: ["PROJ-123"],
  includeAcceptanceCriteria: true,
  includeDescription: true,
  includeTestingChecklist: true,
  targetBranch: "main"
)
```

### Response Fields

| Field | Description |
|-------|-------------|
| `title` | Suggested PR title |
| `body` | Complete PR body markdown |
| `testingChecklist` | Testing items for the PR |
| `suggestedLabels` | Labels based on issue types |
| `reviewersRecommendation` | Review guidance |
| `targetBranch` | Target branch for merge |

### Suggested Labels

Labels are suggested based on issue types:

| Issue Type | Suggested Labels |
|------------|------------------|
| Bug | `bug`, `fix` |
| Story | `feature`, `enhancement` |
| Hotfix | `hotfix`, `urgent` |
| Documentation | `documentation`, `docs` |

### Size Labels

Based on total story points:

| Story Points | Label |
|--------------|-------|
| 1-2 | `size/small` |
| 3-5 | `size/medium` |
| 6+ | `size/large` |

## Creating the PR

After getting context, use gh CLI:

```bash
gh pr create \
  --title "PROJ-123: Add user authentication" \
  --body "$(cat pr-body.md)" \
  --base main \
  --label "feature,size/medium"
```

Or interactively with the generated content.
