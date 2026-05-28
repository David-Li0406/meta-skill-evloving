---
name: git-workflow
description: Use this skill for effective Git version control, including commit conventions, branching strategies, and collaboration best practices.
---

# Git Workflow Best Practices

This document outlines best practices for using Git effectively in version control and collaboration.

## Core Principles
- Write clear, atomic commits that address single logical changes.
- Follow the Conventional Commits specification for all commit messages.
- Use feature branches to isolate changes and enable easier code review.
- Keep branches short-lived and regularly sync with the main branch.
- Never commit directly to the main/master branch.

## Commit Guidelines
### Commit Message Format
Use the following format for all commit messages:
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `build`: Changes that affect the build system or external dependencies
- `ci`: Changes to CI configuration files and scripts
- `chore`: Other changes that don't modify source or test files
- `revert`: Reverts a previous commit

### Commit Message Best Practices
- Use lowercase letters in the entire body of the commit message.
- Keep the commit message title under 60 characters.
- Use imperative mood: "Add feature" not "Added feature."
- Explain the *why* behind the change, not just *what* was changed.
- Reference related issues or tickets in the footer.

## Branching Strategy
### Branch Naming Conventions
Use descriptive, kebab-case branch names with prefixes:
- `feature/` - New features (e.g., `feature/user-authentication`)
- `bugfix/` - Bug fixes (e.g., `bugfix/login-redirect-loop`)
- `hotfix/` - Urgent production fixes (e.g., `hotfix/security-patch`)
- `release/` - Release preparation (e.g., `release/v2.1.0`)
- `docs/` - Documentation updates (e.g., `docs/api-reference`)
- `refactor/` - Code refactoring (e.g., `refactor/database-layer`)

### Workflow Guidelines
1. **Create feature branches from main/develop**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/new-feature
   ```

2. **Keep branches up-to-date**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

3. **Make atomic commits**
   - Each commit should be a single, logical change.
   - Commit early and often when code is in a stable state.
   - Avoid mixing unrelated changes in a single commit.

4. **Before merging**
   - Ensure all tests pass.
   - Squash fixup commits if needed.
   - Rebase onto the latest main to resolve conflicts.

5. **Clean up after merge**
   ```bash
   git branch -d feature/new-feature
   git push origin --delete feature/new-feature
   ```

## Collaboration Guidelines
### Code Review Process
1. Create small, focused pull requests.
2. Write clear PR descriptions explaining the changes.
3. Link related issues and documentation.
4. Request reviews from appropriate team members.
5. Address feedback promptly and professionally.
6. Squash commits when merging if history is messy.

### Merge Strategies
- **Merge commit**: Preserves full history, good for feature branches.
- **Squash and merge**: Combines all commits into one, cleaner main history.
- **Rebase and merge**: Linear history, requires clean commit history.

### Conflict Resolution
1. Pull the latest changes from the target branch.
2. Resolve conflicts locally.
3. Test thoroughly after resolution.
4. Commit with a clear message explaining the resolution.

## Security Best Practices
- Never commit sensitive data (passwords, API keys, tokens).
- Use `.gitignore` to exclude sensitive files.
- Review diffs before committing.
- Use signed commits for verified authorship.
- Rotate any accidentally committed secrets immediately.

## Common Pitfalls
- **Committing Without Reviewing Changes**: Always run `git status` and `git diff` before committing.
- **Vague Commit Messages**: Write clear, descriptive messages following the conventional commit format.
- **Forgetting to Pull Before Push**: Always pull first if working with others.
- **Pushing Directly to Main Without Testing**: Ensure code is tested before merging.
- **Large Binary Files**: Check file sizes before committing and use `.gitignore` for large files.

## Code Snippets/Patterns
### Standard Commit Workflow
```bash
git status
git diff
git add .
git commit -m "feat: implement new feature"
git push origin main
```

### Feature Branch Workflow
```bash
git checkout -b feature/new-feature
git add .
git commit -m "feat: implement new feature"
git push -u origin feature/new-feature
```

### Undo Last Commit (Before Push)
```bash
git reset --soft HEAD~1  # Keep changes, undo commit
git reset --hard HEAD~1  # Discard changes and commit
```

### Check Commit History
```bash
git log --oneline -10
```

### Stash Changes Temporarily
```bash
git stash
git stash pop
```

## Integration with Semantic Versioning
Conventional Commits integrate well with semantic versioning:
- `feat`: triggers a MINOR version bump.
- `fix`: triggers a PATCH version bump.
- `BREAKING CHANGE`: triggers a MAJOR version bump.

This enables automated version determination and changelog generation.