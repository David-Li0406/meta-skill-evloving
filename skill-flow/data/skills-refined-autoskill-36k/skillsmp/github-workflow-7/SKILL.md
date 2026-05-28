---
name: github-workflow
description: GitHub development workflow best practices. Use when creating commits, pull requests, branches, reviewing code, managing issues, or any git/GitHub operations. Provides standards for commit messages, PR descriptions, branch naming, and code review.
---

# GitHub Development Workflow

Best practices for git and GitHub operations in the DOMES project.

## Branch Naming Convention

```
<type>/<short-description>

Types:
- feature/  - New functionality
- fix/      - Bug fixes
- refactor/ - Code restructuring
- docs/     - Documentation only
- test/     - Test additions/changes
- chore/    - Build, CI, tooling changes
```

**Examples:**
- `feature/esp-now-sync`
- `fix/led-driver-timing`
- `refactor/audio-service`
- `docs/api-reference`

**Claude Code branches** follow the pattern: `claude/<task-description>-<id>`

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type (required)
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `docs`: Documentation only
- `test`: Adding or updating tests
- `chore`: Build process, tooling, dependencies
- `perf`: Performance improvement
- `style`: Formatting, missing semicolons (no code change)

### Scope (optional but recommended)
Component or area affected:
- `led`, `audio`, `haptic`, `touch` - Driver components
- `esp-now`, `ble` - Communication
- `game-engine`, `drill` - Application layer
- `build`, `ci` - Infrastructure

### Subject
- Use imperative mood: "add" not "added" or "adds"
- Don't capitalize first letter
- No period at the end
- Max 50 characters

### Body (optional)
- Explain **what** and **why**, not how
- Wrap at 72 characters
- Separate from subject with blank line

### Footer (required for Claude)
```
Co-Authored-By: Claude <name> <version> <noreply@anthropic.com>
```

### Examples

```
feat(led): add brightness scaling with gamma correction

Implement perceptual brightness scaling using a 2.2 gamma lookup
table. This provides smoother visual transitions at low brightness
levels where human perception is most sensitive.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

```
fix(esp-now): prevent packet loss during high-frequency sync

Increase TX queue depth from 4 to 8 and add backpressure handling
when queue is full. Resolves sync failures during 100ms burst tests.

Fixes #42

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## Pull Request Guidelines

### Title Format
Same as commit subject: `<type>(<scope>): <description>`

### PR Description Template

```markdown
## Summary
Brief description of what this PR does (1-3 sentences).

## Changes
- Bullet point list of specific changes
- Be specific about files/components modified
- Note any breaking changes

## Testing
- [ ] Unit tests pass (`idf.py --preview set-target linux && idf.py build`)
- [ ] Builds for ESP32-S3 (`idf.py build`)
- [ ] Tested on hardware (if applicable)
- [ ] No new compiler warnings

## Notes
Any additional context, trade-offs, or follow-up work needed.

---
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### PR Best Practices

1. **Keep PRs small and focused** - One logical change per PR
2. **Self-review first** - Check diff before requesting review
3. **Link issues** - Use "Fixes #123" or "Relates to #123"
4. **Update documentation** - If API changes, update docs
5. **Don't force push after review** - Add fixup commits instead

## Code Review Guidelines

### What to Check

**Functionality:**
- Does it do what the PR claims?
- Are edge cases handled?
- Any potential race conditions?

**DOMES-Specific (embedded):**
- No heap allocation after init?
- ISR-safe if in interrupt context?
- Thread-safe if shared between tasks?
- Const-correct?

**Style:**
- Follows naming conventions?
- Proper documentation on public APIs?
- No magic numbers (use named constants)?

### Review Comments

**Be specific:**
```
// Bad
This could be better.

// Good
Consider using `std::expected` here instead of returning -1,
to match the error handling pattern in other drivers.
See `i_led_driver.hpp:42` for an example.
```

**Suggest, don't demand:**
```
// Softer
Consider: Could we add a bounds check here?

// Harder (use sparingly)
Blocking: This will cause undefined behavior if index > size.
```

## Git Operations

### Before Committing

```bash
# Check what will be committed
git status
git diff --staged

# Ensure no secrets
git diff --staged | grep -i "password\|secret\|key\|token"
```

### Safe Rebasing

```bash
# Update feature branch with main (preferred over merge)
git fetch origin
git rebase origin/main

# If conflicts, resolve then:
git add <resolved-files>
git rebase --continue
```

### Undoing Mistakes

```bash
# Undo last commit (keep changes staged)
git reset --soft HEAD~1

# Undo last commit (keep changes unstaged)
git reset HEAD~1

# Discard all uncommitted changes (DANGEROUS)
git checkout -- .
```

## GitHub CLI (`gh`) Quick Reference

```bash
# Create PR
gh pr create --title "feat(led): add feature" --body "Description"

# List open PRs
gh pr list

# Check out a PR locally
gh pr checkout 123

# View PR status
gh pr status

# Merge PR
gh pr merge 123 --squash

# Create issue
gh issue create --title "Bug: description" --body "Details"

# View issue
gh issue view 123
```

## CI/CD Expectations

Every PR should pass:

1. **Build check** - `idf.py build` succeeds for ESP32-S3
2. **Host tests** - Unit tests pass on Linux target
3. **Static analysis** - No new warnings with `-Wall -Wextra`
4. **Size check** - Binary size doesn't regress significantly

## Protected Branches

- `main` - Production-ready code, requires PR review
- `develop` - Integration branch (if used)

Never force push to protected branches.

## See Also

- [GUIDELINES.md](../../firmware/GUIDELINES.md) - Coding standards
- [MILESTONES.md](../../firmware/MILESTONES.md) - Development milestones
