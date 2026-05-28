# Validation Phase

Verify implementation before submission.

## Setup

Use upstream and default branch. If resuming after session restart:
```bash
# Recover context (sets ISSUE_ID, MOL_ID, ORG_REPO)
source "$SKILL_DIR/resources/scripts/context-recovery.sh"

# Get upstream details (sets UPSTREAM_REMOTE, DEFAULT_BRANCH, UPSTREAM_REF)
source "$SKILL_DIR/resources/scripts/detect-upstream.sh"
```

## Validation Checklist

### 1. Run Tests

From cached `research.yaml` testing commands:
```bash
# Go projects
go test ./...

# Node projects
npm test

# Python projects
pytest

# Or whatever is specified in research.yaml
```

**All tests must pass.** If tests fail:
1. Fix the failures
2. Re-run tests
3. Do not proceed until green

### 2. Run Linters

From cached `research.yaml`:
```bash
# Go
go vet ./...
gofmt -d .

# JavaScript/TypeScript
npm run lint

# Python
ruff check .
```

Fix any linter errors before proceeding.

### 3. Build Check

```bash
# Go
go build ./...

# Node
npm run build

# Verify no build errors
```

### 4. Isolation Check

Verify PR addresses single concern:

```bash
# List changed files
git diff --name-only $UPSTREAM_REF
```

**Isolation criteria:**
- [ ] All changed files relate to issue
- [ ] No unrelated fixes
- [ ] No drive-by improvements
- [ ] Single logical change

If isolation fails:
1. Identify unrelated changes
2. Revert them or move to separate commits
3. Create new issues for discovered work
4. Re-validate

### 5. Rebase Check

Ensure branch is up-to-date with upstream:

```bash
git fetch $UPSTREAM_REMOTE
git log --oneline $UPSTREAM_REF..HEAD  # Our commits
git log --oneline HEAD..$UPSTREAM_REF  # Commits we're behind
```

If behind upstream:
```bash
git rebase $UPSTREAM_REF
# Resolve any conflicts
# Re-run tests after rebase
```

### 6. Commit History Review

```bash
git log --oneline $UPSTREAM_REF..HEAD
```

Verify:
- [ ] Commits are atomic (one logical change each)
- [ ] Messages follow upstream format
- [ ] Issue reference included
- [ ] No WIP or fixup commits

Clean up if needed (use non-interactive commands since -i blocks agents):
```bash
# Squash all commits into one with a new message
git reset --soft $UPSTREAM_REF
git commit -m "type(scope): description (#issue)"

# Or use autosquash for fixup! commits (non-interactive)
git rebase --autosquash $UPSTREAM_REF

# Or squash last N commits
git reset --soft HEAD~N
git commit -m "type(scope): description (#issue)"
```

## Validation Output

After all checks pass:

```
## Validation Results

Tests:      PASSED (42 tests, 0 failures)
Linter:     PASSED (no issues)
Build:      PASSED
Isolation:  PASSED (3 files changed, all related to hq-1234)
Rebased:    Yes (0 commits behind upstream/main)
Commits:    2 commits, clean history

Ready for pre-submit review.
```

## Update Molecule

```yaml
phase: "gate-submit"
validation:
  tests: "passed"
  linter: "passed"
  build: "passed"
  isolation: "passed"
  rebased: true
  commits: 2
  validated_at: "2026-01-19T12:00:00Z"
```

Then **STOP** - proceed to gate-submit (see SKILL.md).

## Validation Failures

### Test Failures

```
Tests: FAILED
  - TestDoctorIndentation: expected 4 spaces, got 2

Action: Fix the failing test before proceeding.
```

Do not proceed. Fix and re-validate.

### Linter Failures

```
Linter: FAILED
  cmd/bd/doctor/database.go:42: missing comment on exported function

Action: Fix linter issues before proceeding.
```

Do not proceed. Fix and re-validate.

### Isolation Failures

```
Isolation: FAILED
  - cmd/bd/doctor/database.go - related to hq-1234 ✓
  - cmd/bd/sync/sync.go - NOT related to hq-1234 ✗

Action: Remove unrelated changes or create separate PR.
```

Options:
1. `git checkout $UPSTREAM_REF -- cmd/bd/sync/sync.go` (revert)
2. Create new issue for the sync changes
3. Re-validate

### Rebase Needed

```
Rebased: NO (5 commits behind upstream/main)

Action: Rebase on upstream default branch before proceeding.
```

```bash
git fetch $UPSTREAM_REMOTE
git rebase $UPSTREAM_REF
# Re-run tests after rebase
```
