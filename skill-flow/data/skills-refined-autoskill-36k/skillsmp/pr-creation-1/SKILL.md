---
name: pr-creation
description: Create and manage GitHub Pull Requests with templates, reviewers, and labels. Use when code is ready for review. Merging requires explicit approval.
license: MIT
compatibility: Requires GitHub CLI (gh) and repository write access
metadata:
  author: ximplicity
  version: "1.0"
  category: git
---

# Pull Request Creation Skill

Create and manage Pull Requests on GitHub.

## Allowed Operations

- Create pull requests
- Update PR description
- Add reviewers
- Add labels
- Request reviews
- View PR status
- View PR comments

## Forbidden Operations

These require explicit approval:

- Merge PRs
- Close PRs without merging
- Delete branches after merge
- Force-approve PRs

## Constraints

- PRs must have a description
- PRs must reference issue/feature ID
- PRs should have at least one reviewer
- Use draft PRs for work-in-progress

## Quick PR Template

```markdown
## Summary

[Brief description of changes]

## Related Issue

Closes: PROJ-123

## Changes

- [Change 1]
- [Change 2]

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
```

For complete templates, see [PR-TEMPLATES.md](references/PR-TEMPLATES.md).

For review guidelines, see [REVIEW-CHECKLIST.md](references/REVIEW-CHECKLIST.md).

## Dry-Run Mode

When `dryRun: true`:
- Validate all PR fields
- Check branch exists
- Verify reviewers exist
- Show PR preview
- Make NO API calls

## Linking

- Link to Jira issues using issue key
- Link to related PRs if applicable
- Reference relevant documentation

## Example Usage

```
Create a PR for branch feature/PROJ-123-login
Add reviewers @alice and @bob to PR #45
Update PR #45 description with test results
Show status of my open PRs
```
