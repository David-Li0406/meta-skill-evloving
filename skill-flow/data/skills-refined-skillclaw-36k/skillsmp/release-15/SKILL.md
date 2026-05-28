---
name: release
description: Release workflow for kasoa monorepo. Supports both CI and local publishing.
---

# Release Workflow

Changesets + npm publishing. CI uses OIDC; local requires npm login + OTP.

## Workflow

### 1. Commit code changes

Use conventional commits: `fix(pkg)`, `feat(pkg)`, `chore:`

### 2. Create changeset

Write `.changeset/<name>.md`:

```markdown
---
"@kasoa/package-name": patch
---

Brief description
```

Semver (pre-1.0): `patch` for fixes/tweaks, `minor` for features/breaking.

### 3. Commit changeset

```bash
git add .changeset/<name>.md && git commit -m "chore: add changeset"
```

### 4. Publish

**Via CI (recommended):**

```bash
git pull --rebase && git push origin main
```

Wait for CI, then merge the Version PR:

```bash
gh pr merge <number> --rebase
```

**Via local:**

Requires: `npm whoami` (must be logged in)

```bash
pnpm changeset version   # versions + auto-commits
pnpm release             # builds + publishes (enter OTP when prompted)
git push origin main --follow-tags
```

### 5. Verify

```bash
npm view <package-name> version
```

## Edge Cases

**Multiple packages:** List all in one changeset file.

**Push rejected:** `git pull --rebase && git push origin main`

**CI fails:** `gh run view <run-id> --log-failed`
