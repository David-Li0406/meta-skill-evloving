---
name: pinpoint-commit
description: Comprehensive commit-to-PR workflow with intelligent testing, branch management, and CI monitoring
---

# PinPoint Commit Skill

Automates the complete commit lifecycle: file review → testing → branching → committing → PR creation → CI monitoring.

## When to Use

Invoke this skill when you're ready to commit and push changes to PinPoint:

- Have uncommitted changes to review
- Need intelligent E2E test selection
- Want conventional commit messages generated
- Creating/updating PRs with detailed descriptions
- Monitoring CI status

## Overview

This skill provides a guided, 6-phase workflow that handles the entire commit-to-PR process with intelligent decision-making and automation.

**Key Features**:

- Smart E2E test selection based on file patterns
- Conventional commit message generation
- Automatic branch validation/creation
- GitHub issue linking support
- PR creation with detailed descriptions
- Optional CI monitoring

---

## Phase 1: Pre-Commit File Review

### 1.1 Check Git Status

Run `git status --porcelain` and categorize files:

**Staged files** (ready to commit):

```
A  src/components/IssueList.tsx
M  src/lib/filters.ts
```

**Unstaged files** (modified but not staged):

```
 M src/server/db/schema.ts
```

**Untracked files** (never committed):

```
?? debug.log
```

### 1.2 Review with User

Present summary:

```
📦 Files ready to commit (staged):
  - src/components/IssueList.tsx
  - src/lib/filters.ts

⚠️  Unstaged changes (not included):
  - src/server/db/schema.ts

❓ Untracked files:
  - debug.log
```

**Ask**:

1. "Include any unstaged files?"
2. "Ignore any untracked files (add to .gitignore)?"

**Actions**:

- `git add <files>` for additional inclusions
- Update `.gitignore` if requested

---

## Phase 2: Testing & Validation

### 2.1 Run Preflight

// turbo
Execute: `pnpm run preflight`

This runs the full validation suite:

- Type checking
- Linting (with auto-fix)
- Formatting (with auto-fix)
- Unit tests
- Config validation
- DB reset
- Build
- Integration tests
- Smoke E2E tests

**If preflight fails**: Show error, offer to run `pnpm run lint:fix && pnpm run format:fix` if it's fixable.

### 2.2 Intelligent E2E Test Selection

Analyze changed files using `git diff --name-only --staged` and recommend test suite based on impact.

**Decision Matrix**:

**High Impact Files** → Recommend `pnpm run e2e:full` (~3-5 min):

- `src/app/(app)/**/page.tsx` - Page components (user journeys)
- `src/app/(app)/**/layout.tsx` - Layout components (site structure)
- `src/app/(auth)/**/*` - Authentication flows
- `src/components/issues/*` - Core issue UI components
- `src/components/machines/*` - Core machine UI components
- `src/server/actions/*` - Server actions (data mutations)
- `src/lib/supabase/*` - Auth/database client
- `supabase/migrations/*` - Database schema changes

**Medium Impact Files** → `pnpm run smoke` (already in preflight):

- `src/components/ui/*` - Reusable UI components
- `src/lib/*` - Utility libraries
- `src/server/db/schema.ts` - Schema definitions

**Low Impact Files** → Skip additional E2E:

- `docs/**/*` - Documentation
- `*.test.ts` - Test files
- `*.spec.ts` - E2E test files
- `.agent/**/*` - Agent skills
- `scripts/*` - Build/dev scripts

**Present recommendation**:

```
Based on your changes to:
  - src/app/(app)/issues/page.tsx (page component - HIGH IMPACT)
  - src/components/IssueList.tsx (core UI - HIGH IMPACT)

I recommend: pnpm run e2e:full

This will add ~3-5 minutes but ensures user journeys work.

Run full E2E suite? (y/n)
```

**If approved**:
// turbo

```bash
pnpm run e2e:full
```

---

## Phase 3: Branch Management

### 3.1 Check Current Branch

```bash
git rev-parse --abbrev-ref HEAD
```

**Branch types**:

- ✅ **Feature branches**: `feature/*`, `fix/*`, `chore/*`, `docs/*`
- ⚠️ **Main branch**: Don't commit directly
- ❌ **Detached HEAD**: Create a branch first

### 3.2 Handle Branch Scenarios

**Scenario A: On `main`**

```
⚠️  You're on main. PinPoint policy: work on feature branches.
I'll create a new branch for you.
```

→ Jump to **3.3 Create Branch**

**Scenario B: Detached HEAD**

```
❌ Detached HEAD state. Creating a branch...
```

→ Jump to **3.3 Create Branch**

**Scenario C: Valid feature branch**

```
✅ On branch: feature/issue-filter-search
Proceeding...
```

→ Continue to **Phase 4**

### 3.3 Create New Branch

Analyze changed files to suggest a name:

```
Changed files: src/components/IssueList.tsx, src/lib/filters.ts
→ Suggest: feature/issue-list-filters
```

**Ask user**:

```
Creating new branch off main.
Suggested: feature/issue-list-filters

Options:
1. Use suggested name
2. Enter custom name
3. Enter GitHub issue # (I'll format as "feature/123-description")
```

**Create**:

```bash
git checkout -b <branch-name> main
```

---

## Phase 4: Commit Message Generation

### 4.1 Generate Message

Analyze staged changes using `git diff --staged --stat` and `git diff --staged --name-only` to generate a conventional commit message.

**Conventional Commits format**: `<type>(<scope>): <description>`

**Type Selection** (analyze changed files):

- `feat` - New features (new components, new routes, new functionality)
- `fix` - Bug fixes (fix typos, fix logic errors, fix crashes)
- `refactor` - Code restructuring (extract hooks, extract components, reorganize)
- `chore` - Maintenance (dependency updates, config changes, tooling)
- `docs` - Documentation only (README, comments, doc files)
- `test` - Test additions/changes (new tests, test fixes)
- `style` - Formatting only (prettier, lint fixes without logic changes)

**Scope Selection** (primary area of changes):

Look at changed file paths and use:

- `issues` - src/components/issues/_, src/app/(app)/issues/_
- `machines` - src/components/machines/_, src/app/(app)/m/_
- `auth` - src/app/(auth)/_, src/lib/supabase/_
- `ui` - src/components/ui/\*
- `db` - supabase/migrations/_, src/server/db/_
- `e2e` - e2e/\*_/_
- `agents` - .agent/\*_/_

**Body Generation**:

Use `git diff --staged --stat` output to create bullet points:

- Group by category: "Bug Fixes", "Features", "Refactoring", "Documentation", "Testing"
- Be specific about what changed
- Mention notable file changes
- Include impact (+X/-Y lines)

### 4.2 Review with User

**Present**:

```
Generated commit message:

  feat(issues): Update issues functionality

  - Update 3 source file(s)
  - Add/update 2 test(s)

Stats: +42/-10 lines

Options:
1. Use this message
2. Edit the message
3. Add "Closes #" reference
```

### 4.3 Add Issue Reference (Optional)

If user wants to link an issue:

```bash
gh issue list --limit 20 --json number,title
```

Present recent issues, append `Closes #<issue>` to commit body.

### 4.4 Commit

```bash
git commit -m "<title>" -m "<body>"
```

---

## Phase 5: Push & PR Management

### 5.1 Check Upstream & Push

Check if remote branch exists:

```bash
git rev-parse --abbrev-ref @{upstream} 2>/dev/null
```

**If doesn't exist**:

```bash
git push -u origin <branch-name>
```

**If exists**:

```bash
git push
```

### 5.2 Check for Existing PR

```bash
gh pr list --head <branch-name> --json number,url,state
```

**If PR exists**:

```
✅ Found PR #123
URL: https://github.com/timothyfroehlich/PinPoint/pull/123

Pushed new commits.
Continue to CI monitoring? (y/n)
```

**If no PR**: → Continue to **5.3 Create PR**

### 5.3 Create PR

**Generate description**:

```markdown
## Summary

[1-2 sentence overview from commit message]

## Changes

- [Bullet from commit body]
- [Bullet from commit body]

## Testing

- ✅ Unit tests: passing
- ✅ Integration tests: passing
- ✅ E2E tests: [suite run]

## Related Issues

Closes #[issue] (if provided)

## Checklist

- [x] Preflight passed locally
- [x] Tests added/updated
- [ ] CI checks pending...
```

**Ask user**:

```
Generated PR description.

Options:
1. Create PR
2. Edit description
3. Create as DRAFT
```

**Create**:

```bash
# Regular PR
gh pr create --title "<title>" --body "<description>"

# Draft PR
gh pr create --title "<title>" --body "<description>" --draft
```

---

## Phase 6: CI Monitoring (Optional)

**Ask user**:

```
PR #123 created!
URL: https://github.com/timothyfroehlich/PinPoint/pull/123

Monitor GitHub Actions?
Max wait: 10 minutes

Options:
1. Watch CI (block until complete)
2. Skip monitoring
```

### 6.1 Watch CI

Poll GitHub Actions status using `gh pr checks <pr-number>`:

```bash
# Check current status
gh pr checks <pr-number>

# Poll every 30 seconds for up to 10 minutes
# Show status updates to user
```

**Status check output format**:

```
✓ Preflight          pass  2m 15s
✓ Build             pass  1m 45s
○ E2E Tests         pending
× Playwright        fail
```

**Parse and present**:

```
⏳ Monitoring CI for PR #123...
[00:30] Checks: 2/4 complete, 2 passed, 0 failed
[01:00] Checks: 3/4 complete, 3 passed, 0 failed
[03:00] Checks: 4/4 complete, 4 passed, 0 failed

✅ All CI checks passed! (3m 0s)
```

**On success**:

```
✅ All checks passed!

Your PR is ready for review.

Next steps:
1. Request review: gh pr review <pr> --request @reviewer
2. View PR: gh pr view <pr> --web
```

**On failure**:

```
❌ CI checks failed

Failed checks:
  - E2E Tests / Playwright (chromium)

View details: gh pr checks <pr-number>
```

**On timeout**:

```
⏱️  Timeout after 10 minutes.
Some checks still running.

View: gh pr checks <pr-number>
```

---

## Final Summary

**Present complete summary**:

```
🎉 Workflow Complete!

✅ Committed: feat(issues): Update issues functionality
✅ Pushed to: origin/feature/issue-list-filters
✅ PR Created: #123 (https://github.com/timothyfroehlich/PinPoint/pull/123)
✅ CI Status: All checks passing

Next Steps:
  - Request review: gh pr review 123 --request
  - View PR: gh pr view 123 --web

Your code is ready for team review! 🚀
```

---

## Turbo Mode

Steps marked `// turbo` auto-run without approval:

- `pnpm run preflight`
- `pnpm run e2e:full` (if user approved)
- `git push`
- CI monitoring commands

---

## Best Practices

### When to Use This Skill

✅ **Use when**:

- Ready to commit and push work
- Want structured, validated workflow
- Creating PRs with good descriptions
- Need test recommendations

❌ **Don't use when**:

- Just exploring/experimenting
- Making tiny documentation fixes
- Working on throwaway branches

### Pro Tips

1. **Run frequently**: Don't wait to accumulate many changes
2. **Trust the decision matrix**: High-impact files need full E2E coverage
3. **Edit commit messages**: Generated messages are a starting point
4. **Link issues**: Helps track which PRs close which issues
5. **Watch CI**: Catch failures early before requesting review

---

## Integration with Other Tools

### GitHub CLI (gh)

Required for:

- PR creation and management
- Issue linking
- CI monitoring

Install: `npm install -g gh` or use system package manager

### PinPoint Scripts

Leverages:

- `pnpm run preflight` - Full validation suite
- `pnpm run e2e:full` - Complete E2E tests
- `pnpm run smoke` - Fast smoke tests

### Git Hooks

Works with Husky pre-commit hooks:

- `lint-staged` runs on commit
- Formatting auto-applied
- Process transparent to user
