---
name: pull-request
description: >
  Pull request conventions and workflow for MuebleriaIris.
  Trigger: When creating PRs, reviewing code, or managing Git workflow.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Creating pull requests"
    - "Reviewing code changes"
    - "Managing Git branches"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Creating pull requests
- Reviewing code changes
- Managing Git branches
- Writing commit messages
- Merging branches

---

## Git Workflow

```
1. Create feature branch from main
2. Make changes + commit
3. Push to remote
4. Create pull request
5. Code review
6. Merge to main
```

---

## Critical Patterns

### Pattern 1: Branch Naming

```bash
# Feature branches
feature/add-product-filter
feature/inventory-alerts

# Bug fixes
fix/product-validation
fix/order-stock-deduction

# Improvements
improve/api-error-handling
improve/ui-responsiveness

# Documentation
docs/api-endpoints
docs/setup-guide
```

### Pattern 2: Commit Messages

```bash
# Format: <type>(<scope>): <description>

# Good commits
feat(products): add image upload endpoint
fix(orders): prevent negative stock
docs(readme): update setup instructions
style(ui): improve button spacing
refactor(api): extract validation logic
test(orders): add stock deduction tests

# Bad commits
update stuff
fix bug
changes
wip
```

### Pattern 3: PR Template

```markdown
## Description

Brief description of what this PR does.

## Type of Change

- [ ] New feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Refactoring
- [ ] Testing

## Changes Made

- Added product image upload
- Updated validation logic
- Fixed stock deduction bug

## Testing

- [ ] Tested locally
- [ ] Unit tests pass
- [ ] E2E tests pass
- [ ] Tested on mobile

## Screenshots (if UI changes)

![Screenshot](url)

## Checklist

- [ ] Code follows project style
- [ ] Self-reviewed code
- [ ] Commented complex logic
- [ ] Updated documentation
- [ ] No console errors
```

---

## Git Commands

```bash
# Create and switch to new branch
git checkout -b feature/my-feature

# Stage changes
git add .

# Commit with message
git commit -m "feat(products): add filter by category"

# Push to remote
git push origin feature/my-feature

# Create PR (using GitHub CLI)
gh pr create --title "Add product filter" --body "..."

# Update branch with main
git checkout main
git pull origin main
git checkout feature/my-feature
git merge main

# Alternative: rebase
git rebase main

# Squash commits before merge
git rebase -i HEAD~3
```

---

## Code Review Checklist

### For Reviewers

- [ ] Code follows project conventions
- [ ] No hardcoded credentials
- [ ] Error handling present
- [ ] Tests cover new functionality
- [ ] No breaking changes
- [ ] Documentation updated
- [ ] Performance considerations
- [ ] Security vulnerabilities

### Common Review Comments

```markdown
# Suggest improvement
**Suggestion:** Extract this logic into a separate function

# Request change
**Change needed:** Add error handling for this API call

# Ask question
**Question:** Why did we choose this approach?

# Approve with nit
**LGTM** (Looks Good To Me) with minor nit: rename variable

# Request tests
**Tests:** Can you add tests for this edge case?
```

---

## Pull Request Best Practices

### DO:
- Keep PRs small and focused (< 400 lines)
- Write descriptive PR titles
- Link related issues (#123)
- Test before submitting
- Respond to review comments
- Squash WIP commits

### DON'T:
- Mix unrelated changes
- Submit untested code
- Ignore review feedback
- Force push after review
- Leave TODO comments
- Include debug code

---

## Merge Strategies

```bash
# Squash and merge (preferred for feature branches)
# Combines all commits into one
git merge --squash feature/my-feature

# Regular merge (for release branches)
git merge feature/my-feature

# Rebase and merge (clean history)
git rebase main
git checkout main
git merge feature/my-feature
```

---

## Resolving Conflicts

```bash
# When merge conflicts occur
git merge main
# Fix conflicts in files
git add .
git commit -m "Merge main into feature"
git push

# Using VS Code
# 1. Open conflicted file
# 2. Choose: Accept Current | Accept Incoming | Accept Both
# 3. Save and commit
```

---

## Commands

```bash
# Create branch
git checkout -b feature/name

# Commit
git add .
git commit -m "feat: description"

# Push
git push origin feature/name

# Create PR (GitHub CLI)
gh pr create

# View PRs
gh pr list

# Checkout PR locally
gh pr checkout 123

# Merge PR
gh pr merge 123 --squash
```

---

## QA Checklist

- [ ] Branch name follows convention
- [ ] Commits are descriptive
- [ ] PR has clear description
- [ ] Tests pass (npm test, pytest)
- [ ] No merge conflicts
- [ ] Code is self-reviewed
- [ ] Documentation updated
- [ ] Screenshots for UI changes

---

## Resources

- **GitHub Flow**: https://guides.github.com/introduction/flow/
- **Conventional Commits**: https://www.conventionalcommits.org
