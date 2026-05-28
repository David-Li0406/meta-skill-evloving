# PR and Code Review Workflow

## Overview

This document outlines the pull request and code review workflow for ROLESENSE.ai development. Issues created with the github-issue-creator skill are designed to support this workflow seamlessly.

---

## Workflow Stages

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Issue     │───▶│   Branch    │───▶│     PR      │───▶│   Review    │───▶│   Merge     │
│  Created    │    │  Created    │    │  Created    │    │  Complete   │    │  to Main    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## Stage 1: Issue Assignment

### Prerequisites
- Issue exists with proper template (Epic, Feature, Subtask, Bug)
- Issue has appropriate labels and milestone
- Issue has acceptance criteria defined

### Actions
1. Developer self-assigns or is assigned to issue
2. Developer reviews linked documentation
3. Developer confirms understanding of requirements

### Checklist
- [ ] Issue assigned
- [ ] Documentation reviewed (FR spec, workflow, UI/UX spec)
- [ ] Questions clarified with team if needed
- [ ] Acceptance criteria understood

---

## Stage 2: Branch Creation

### Branch Naming Convention

```
{Sprint}-{Feature-Name}
```

**Examples:**
| Issue Type | Branch Name |
|------------|-------------|
| Sprint Epic | `Sprint2-Resume-Ingestion` |
| Feature | `Sprint2-Resume-Ingestion` (same as epic) |
| Bug fix | `Sprint2-Resume-Ingestion` or `fix/upload-validation` |
| Hotfix | `hotfix/critical-auth-bug` |

### Commands

```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Create feature branch
git checkout -b Sprint2-Resume-Ingestion

# Push branch to remote
git push -u origin Sprint2-Resume-Ingestion
```

### Branch Rules
- Always branch from latest `main`
- One branch per Epic (subtasks work on same branch)
- Keep branches short-lived (< 1 week ideal)

---

## Stage 3: Development

### Commit Message Convention

```
{type}({scope}): {description}

[optional body]

[optional footer]
Refs: #{issue_number}
```

### Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(resume): add file upload endpoint` |
| `fix` | Bug fix | `fix(upload): handle empty file error` |
| `docs` | Documentation | `docs(api): add OpenAPI specs` |
| `style` | Formatting | `style(ui): apply design tokens` |
| `refactor` | Code restructure | `refactor(parser): extract validation logic` |
| `test` | Tests | `test(upload): add integration tests` |
| `chore` | Maintenance | `chore(deps): update boto3` |

### Commit Examples

```bash
# Feature commit
git commit -m "feat(resume): add file upload endpoint

Implements POST /api/v1/resumes/upload with:
- Multipart form handling
- MIME type validation
- MinIO storage integration

Refs: #42"

# Bug fix commit
git commit -m "fix(upload): validate file size before processing

Prevents server errors when files exceed 10MB limit.

Refs: #45"

# Test commit
git commit -m "test(upload): add unit tests for validation service

Adds tests for:
- MIME type checking
- File size validation
- Magic number verification

Coverage: 85%

Refs: #42"
```

### Development Checklist
- [ ] Code follows project style guide
- [ ] Unit tests written for new code
- [ ] Integration tests updated if needed
- [ ] No console.log or debug statements
- [ ] Environment variables documented
- [ ] API changes reflected in OpenAPI spec

---

## Stage 4: Pull Request Creation

### PR Title Format

```
{type}({scope}): {description} (#{issue_number})
```

**Examples:**
- `feat(resume): implement multi-format upload (#42)`
- `fix(auth): resolve session timeout (#38)`

### PR Description Template

```markdown
## Summary

Brief description of changes (1-2 sentences).

## Related Issue

Closes #{issue_number}

## Changes

### Backend
- Change 1
- Change 2

### Frontend
- Change 1
- Change 2

### Tests
- Unit tests added for X
- Integration tests for Y

## Screenshots (if UI changes)

| Before | After |
|--------|-------|
| [image] | [image] |

## Checklist

### Code Quality
- [ ] Code follows project style guide
- [ ] No linting errors
- [ ] No TypeScript errors
- [ ] Self-reviewed the code

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests pass
- [ ] Manual testing completed

### Documentation
- [ ] API documentation updated (if applicable)
- [ ] Component documentation updated (if applicable)
- [ ] README updated (if applicable)

### UI/UX (if frontend changes)
- [ ] Matches design spec (Section X.X)
- [ ] Responsive design verified
- [ ] Accessibility checked
- [ ] Design tokens applied

### Database (if schema changes)
- [ ] Migration created
- [ ] Rollback tested
- [ ] Data integrity verified

## Deployment Notes

Any special deployment considerations (environment variables, migrations, etc.)

## Testing Instructions

Steps for reviewers to test the changes:
1. Step 1
2. Step 2
3. Expected result
```

### Creating the PR

```bash
# Using GitHub CLI
gh pr create --title "feat(resume): implement multi-format upload (#42)" \
  --body-file .github/PR_TEMPLATE.md \
  --base main \
  --head Sprint2-Resume-Ingestion

# Or via GitHub UI
# Navigate to repository → Pull Requests → New Pull Request
```

### PR Labels

| Label | When to Use |
|-------|-------------|
| `ready-for-review` | PR is complete and ready |
| `wip` | Work in progress, not ready |
| `needs-tests` | Missing test coverage |
| `needs-docs` | Missing documentation |
| `breaking-change` | Contains breaking changes |

---

## Stage 5: Code Review

### Reviewer Assignment
- At least 1 reviewer required
- 2 reviewers for critical paths (auth, payments, data)
- Auto-assign based on CODEOWNERS file

### Review Checklist

```markdown
## Code Review Checklist

### Functionality
- [ ] Code does what the issue requires
- [ ] Edge cases handled
- [ ] Error handling appropriate
- [ ] No obvious bugs

### Code Quality
- [ ] Clear and readable
- [ ] DRY (no unnecessary duplication)
- [ ] SOLID principles followed
- [ ] Appropriate abstractions

### Testing
- [ ] Adequate test coverage
- [ ] Tests are meaningful (not just for coverage)
- [ ] Edge cases tested
- [ ] Error scenarios tested

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Authentication/authorization correct
- [ ] No SQL injection vulnerabilities

### Performance
- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] No memory leaks
- [ ] Efficient algorithms

### Documentation
- [ ] Code comments where needed
- [ ] API documentation complete
- [ ] Complex logic explained
```

### Review Comments

**Constructive feedback format:**
```
[Type] Description

Suggestion: Alternative approach

Example: Code snippet if helpful
```

**Comment Types:**
| Prefix | Meaning | Action Required |
|--------|---------|-----------------|
| `[Required]` | Must fix before merge | Yes |
| `[Suggestion]` | Nice to have improvement | No |
| `[Question]` | Seeking clarification | Response needed |
| `[Nitpick]` | Minor style preference | No |

### Review Outcomes

| Outcome | Description | Next Step |
|---------|-------------|-----------|
| ✅ Approved | Ready to merge | Proceed to merge |
| 🔄 Changes Requested | Issues to address | Fix and re-request |
| 💬 Comment | Questions/discussion | Respond and clarify |

---

## Stage 6: Addressing Review Feedback

### Process
1. Read all feedback carefully
2. Respond to each comment
3. Make requested changes
4. Push new commits (don't force-push during review)
5. Re-request review

### Response Guidelines

```markdown
# Addressing feedback

## [Required] Fix validation logic
Done in commit abc1234

## [Suggestion] Use early return
Implemented, good catch!

## [Question] Why async here?
This allows concurrent file processing. Added comment to clarify.

## [Nitpick] Naming preference
Kept current naming for consistency with existing codebase.
```

---

## Stage 7: Merge

### Pre-Merge Checklist
- [ ] All reviews approved
- [ ] CI/CD pipeline passing
- [ ] No merge conflicts
- [ ] Branch up to date with main

### Merge Strategy

**Squash and Merge (Preferred)**
- Combines all commits into single commit
- Cleaner history
- Use PR title as commit message

```bash
# Via GitHub UI: "Squash and merge" button

# Via CLI
gh pr merge --squash --delete-branch
```

### Post-Merge Actions
1. Delete feature branch
2. Close related issue (automatic if PR uses "Closes #XX")
3. Update project board status
4. Notify team in Slack/Discord if significant change

---

## CI/CD Integration

### Required Checks

```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on: [pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lint
        run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Test
        run: npm run test:coverage

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: npm run build
```

### Branch Protection Rules

- Require PR reviews before merging
- Require status checks to pass
- Require branches to be up to date
- Include administrators in rules

---

## Quick Reference

### Common Git Commands

```bash
# Update branch with latest main
git checkout main
git pull origin main
git checkout Sprint2-Resume-Ingestion
git merge main

# Resolve conflicts
git status  # See conflicted files
# Edit files to resolve
git add .
git commit -m "chore: resolve merge conflicts"

# Interactive rebase (before PR, if needed)
git rebase -i main

# Push changes
git push origin Sprint2-Resume-Ingestion
```

### GitHub CLI Commands

```bash
# Create PR
gh pr create --title "feat: description" --body "details"

# View PR status
gh pr status

# Check out PR locally
gh pr checkout 42

# Merge PR
gh pr merge --squash --delete-branch

# View PR checks
gh pr checks
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Merge conflicts | Rebase from main, resolve conflicts |
| CI failing | Check logs, fix issues, push new commit |
| Review stalled | Ping reviewers, escalate if needed |
| Branch out of date | Merge or rebase from main |

### Getting Help

1. Check project documentation
2. Ask in team Slack channel
3. Pair with senior developer
4. Escalate to tech lead
