---
name: final-review
description: Performs a comprehensive pre-merge review of changes on the current branch. Use when the user wants to verify their work before merging, check PR readiness, or run a final validation of tests, types, lint, and PR metadata.
---

# Final Review Skill

Pre-merge review: `/final-review`

**Fix issues immediately without asking permission.** Report what was done.

## Process

### 0. Fetch Latest

Run `git fetch origin main` to ensure comparisons use the latest main branch.

### 1. Test Coverage

- Run `git diff main --name-only` to identify changed files
- Confirm each core module (`src/*.rs` excluding test modules) has corresponding tests
- Current modules requiring tests: `loader.rs`, `executor.rs`, `state.rs`
- Note: `main.rs`, `lib.rs`, `templates.rs`, and `src/commands/` do not require separate unit tests
- Run `cargo test`

**Fix:** Write missing tests, fix failing tests, re-run until green.

### 2. Build Verification

```bash
cargo fmt --check && cargo clippy -- -D warnings && cargo test && cargo build --release
```

This matches the CI pipeline defined in `.github/workflows/ci.yml`.

**Fix:** Resolve format errors, lint errors, test failures:

- `cargo fmt` - auto-fix formatting issues
- Fix clippy warnings manually

Re-run the verification commands until zero errors.

### 3. Documentation Consistency

Verify all documentation sources are consistent:

- `README.md` - User-facing documentation (installation, usage, CLI reference)
- `CLAUDE.md` - Developer documentation (commands, architecture, development setup)

Check for:

- CLI commands and options match between docs and `src/main.rs`
- Architecture section lists all modules in `src/`
- Example code is accurate and runnable

**Fix:** Update any inconsistent or stale documentation.

### 4. Version Update

Check `Cargo.toml` version against change scope:

- **Major:** Breaking changes (removed features, incompatible API changes)
- **Minor:** New features (new CLI commands, new public API functions)
- **Patch:** Bug fixes, documentation updates, refactoring

Any user-facing change requires at least a patch bump.

**Important:** This crate is published to crates.io automatically. When the version in `Cargo.toml` changes on main:
1. CI detects the version bump
2. Creates a git tag `v<version>`
3. Creates a GitHub Release with auto-generated changelog
4. Publishes to crates.io

To trigger a release, simply bump the version in `Cargo.toml` before merging.

**Fix:** Update version in `Cargo.toml` if needed.

### 5. PR Metadata (if PR exists)

- `gh pr view` - check current title/description
- `git log main..HEAD --oneline` - see commits
- `git diff main --stat` - see change scope

**Fix:** Use `gh pr edit --title` and `gh pr edit --body` to update.

### 6. Commit and Push

Stage, commit, and push all fixes made during review.

## Output

```
## Final Review Results

### Test Coverage
[x] Unit tests exist for core modules
[x] All tests pass
Changes: <tests added/fixed>

### Build Status
[x] fmt/clippy/test/build all pass
Changes: <code fixes>

### Documentation Consistency
[x] README.md and CLAUDE.md are consistent
Changes: <doc updates>

### Version Update
[x] Version updated appropriately
Changes: <version bump type or "no change needed">

### PR Metadata
[x] Title and description accurate
Changes: <PR updates>

### Commits
<commits created>

## Verdict: READY TO MERGE | NEEDS MANUAL ATTENTION
```
